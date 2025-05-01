from pathlib import Path
import os
import sys
import json
from talon import actions, cron
from talon.experimental.parrot import ParrotFrame
from talon_init import TALON_USER

patterns_json = None

def get_talon_user_path():
    """Get the talon user path based on the platform."""
    if sys.platform == "win32":
        return os.path.join(os.getenv("APPDATA"), "talon", "user")
    else:
        return os.path.join(os.getenv("HOME"), ".talon", "user")

def get_parrot_integration_path():
    """Get the path to the parrot_integration.py file."""
    talon_user_path = get_talon_user_path()
    matches = list(Path(talon_user_path).rglob("parrot_integration.py"))

    for path in matches:
        print("Found parrot_integration.py:", path)

    return matches[0] if matches else None

def get_patterns_py_path():
    """Get the path to the patterns.py file."""
    talon_user_path = get_talon_user_path()
    matches = list(Path(talon_user_path).rglob("patterns.json"))

    for path in matches:
        print("Found patterns.json:", path)

    return matches[0] if matches else None

def load_patterns(path: Path) -> dict:
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"❌ Failed to load patterns from {path}: {e}")
        return {}

def build_relative_import_path(current_file: Path, target_file: Path) -> str:
    # Root of all Talon scripts
    user_root = Path.home() / ".talon" / "user"
    if not all(part.isidentifier() for part in target_file.parts):
        raise ValueError(f"Invalid import path — folder/file names must be valid Python identifiers: {target_file}")

    # Determine how many levels up we need to go from current file
    up_levels = len(current_file.parts) - 1
    dot_prefix = "." * up_levels if up_levels > 0 else "."

    # Module path: foo/bar/baz.py → foo.bar.baz
    target_module = ".".join(target_file.parts)

    return f"{dot_prefix}.{target_module}"

class Buffer:
    def __init__(self, size: int = 5):
        self.size = size
        self.buffer: list[ParrotFrame] = []
        self.buffer_last: list[ParrotFrame] = []
        self.get_time_window = 0.3

    def add(self, item):
        if len(self.buffer) > self.size:
            self.buffer_last = self.buffer.copy()
            self.buffer = []
        self.buffer.append(item)

    def get(self, current_ts: float) -> list[ParrotFrame]:
        all = self.buffer_last + self.buffer
        # look at each frame.ts and get the last 0.3 seconds
        return [frame for frame in all if current_ts - frame.ts < self.get_time_window]

    def clear(self):
        """Clear the buffer."""
        self.buffer = []
        self.buffer_last = []

buffer = Buffer()

class Capture:
    def __init__(self, detect_frame: ParrotFrame):
        self.frames = buffer.get(detect_frame.ts)
        self.frames.append(detect_frame)
        detect_frame_index = len(self.frames) - 1
        self.detect_frames = [(detect_frame, detect_frame_index)]

    def add_frame(self, frame: ParrotFrame):
        self.frames.append(frame)

    def add_detect_frame(self, frame: ParrotFrame):
        self.frames.append(frame)
        detect_frame_index = len(self.frames) - 1
        self.detect_frames.append((frame, detect_frame_index))

class CaptureCollection:
    capture_timeout = "350ms"
    max_frames_per_capture = 50

    def __init__(self):
        self.current_capture: Capture | None = None
        self.captures: list[Capture] = []
        self.end_current_capture_job = cron.after(self.capture_timeout, self.end_current_capture)

    def add(self, frame: ParrotFrame, active: set[str]):
        if self.current_capture and len(self.current_capture.frames) >= self.max_frames_per_capture:
            self.end_current_capture()

        if active:
            if self.current_capture is None:
                self.current_capture = Capture(frame)
                self.captures.append(self.current_capture)
            else:
                self.current_capture.add_detect_frame(frame)
            if self.end_current_capture_job is not None:
                cron.cancel(self.end_current_capture_job)
            self.end_current_capture_job = cron.after(self.capture_timeout, self.end_current_capture)
        elif self.current_capture is not None:
            self.current_capture.add_frame(frame)

    def end_current_capture(self):
        if self.current_capture is not None:
            self.current_capture = None
            if self.end_current_capture_job is not None:
                cron.cancel(self.end_current_capture_job)
            self.end_current_capture_job = None
            # print("ui_elements_set_state captures", self.captures)
            # print("last_capture", self.captures[-1])
            print("last_capture.frames", len(self.captures[-1].frames))
            # actions.user.ui_elements_set_state("captures", self.captures)

    def clear(self):
        self.captures = []
        self.current_capture = None
        if self.end_current_capture_job is not None:
            cron.cancel(self.end_current_capture_job)
            self.end_current_capture_job = None

capture_collection = CaptureCollection()

def reset_capture_collection():
    buffer.clear()
    capture_collection.clear()

def wrap_pattern_match(parrot_delegate):
    def wrapper(frame: ParrotFrame):
        buffer.add(frame)


        # print("items", frame.classes.items())
        # winner_label, winner_prob = next(iter(frame.classes.items()))
        # print('parrot', f"predict {winner_label} {winner_prob * 100:.2f}% pow={frame.power:.2f} f0={frame.f0:.3f} f1={frame.f1:.3f} f2={frame.f2:.3f}")

# ----------------------
# parrot top classes: [('pop', 100.0), ('ah', 0.0), ('cough', 0.0)] pow=32.87
# items dict_items([('pop', 0.9999999548035842), ('Background', 2.165785893320523e-08), ('Palate', 1.5241312818179763e-08), ('Alveolar click', 7.659650552614123e-09), ('cough', 5.612743541676491e-10), ('ah', 7.171657493492731e-11), ('oh', 4.548153815911422e-12), ('guh', 3.61841299598122e-14), ('oo', 1.8182810749520447e-14), ('ay', 2.784034513747668e-17), ('tut', 1.9871532056387624e-17), ('t', 1.5135993326208248e-18), ('er', 5.324800770665644e-19), ('ss', 1.494661187376545e-19), ('eh', 1.7080195569776828e-20), ('nn', 1.026558318555397e-20), ('yi', 5.416413802189067e-22), ('sh', 7.765702632204921e-24)])
# items dict_items([('pop', 0.9999999846754178), ('Background', 1.2393125625517942e-08), ('ah', 2.322735986684431e-09), ('cough', 3.3349614880916044e-10), ('Alveolar click', 2.6987391154625106e-10), ('Palate', 4.9716768067690575e-12), ('guh', 2.7858951038453935e-13), ('oh', 9.531912966449682e-14), ('oo', 4.675429006160494e-15), ('tut', 1.436627495199872e-16), ('t', 8.809946695818598e-18), ('ss', 9.586098251575243e-19), ('ay', 9.211563160822906e-19), ('eh', 2.5303787519838825e-20), ('nn', 2.560179452031265e-21), ('er', 1.52536384449555e-21), ('yi', 4.402646498996859e-22), ('sh', 5.8318629457461604e-24)])
# items dict_items([('oh', 0.5914741993986102), ('cough', 0.2255248105578589), ('ah', 0.13144136835024406), ('oo', 0.0261492774566294), ('guh', 0.02352345844034715), ('eh', 0.0009240689317374044), ('Alveolar click', 0.0006187370152434107), ('tut', 0.00022857814261570617), ('yi', 0.00010339032215052213), ('pop', 5.3079352440697015e-06), ('sh', 3.592782477518725e-06), ('ss', 2.4857938929837977e-06), ('t', 3.968366278467488e-07), ('Palate', 2.414680740950413e-07), ('ay', 4.771567470642449e-08), ('Background', 3.406923016462561e-08), ('er', 4.7295223992581166e-09), ('nn', 5.381940872274235e-11)])
# items dict_items([('pop', 0.9999828094483583), ('ah', 1.5447215809496334e-05), ('oh', 5.21354296355757e-07), ('guh', 4.382389077193658e-07), ('Palate', 4.25242549157762e-07), ('oo', 1.7717203533903665e-07), ('Alveolar click', 1.5165485415393918e-07), ('cough', 1.586143440422091e-08), ('Background', 1.3740296808965544e-08), ('tut', 7.048778509827473e-11), ('ay', 6.688146594197927e-13), ('nn', 1.46122621877921e-13), ('ss', 1.4054086081828236e-13), ('yi', 5.9498847802880095e-15), ('eh', 4.7764339895571834e-15), ('er', 2.5307306590034157e-15), ('sh', 1.0317075920400623e-15), ('t', 5.609236520136087e-16)])
# ----------------------
# parrot top classes: [('pop', 100.0), ('ah', 0.0), ('oh', 0.0)] pow=13.26
# items dict_items([('pop', 0.9898505071094219), ('Alveolar click', 0.008601861734565442), ('Background', 0.00047913911763609646), ('cough', 0.00033413507947105045), ('ah', 0.000253027139045097), ('guh', 0.0002478005747371762), ('oo', 0.000136367917477125), ('Palate', 9.074484555945427e-05), ('oh', 6.395508672757065e-06), ('tut', 1.7233525095029524e-08), ('t', 3.0611238950287486e-09), ('nn', 4.67052570095662e-10), ('ay', 1.8769643984134427e-10), ('er', 9.587587721870889e-12), ('sh', 6.813871732108521e-12), ('yi', 4.7464455035878584e-12), ('ss', 2.4518047718457386e-12), ('eh', 4.16291132286715e-13)])
# items dict_items([('guh', 0.9961801866069695), ('t', 0.0015854724514975064), ('ss', 0.0013497915141723773), ('cough', 0.0006818168529740076), ('sh', 0.0001067191876880657), ('eh', 7.886462521375045e-05), ('yi', 8.685874149610155e-06), ('oh', 3.724892347876175e-06), ('Palate', 2.7624242854944804e-06), ('oo', 1.385635632716075e-06), ('tut', 2.8493314986042246e-07), ('Background', 1.4967700177617187e-07), ('ah', 8.487199429491438e-08), ('ay', 4.306342136653478e-08), ('pop', 1.548128649952846e-08), ('Alveolar click', 7.183922614426278e-09), ('er', 3.901590230505913e-09), ('nn', 8.227023356068868e-10)])
# items dict_items([('pop', 0.9999956445764934), ('oh', 2.570183670428357e-06), ('cough', 7.535003498935534e-07), ('Alveolar click', 4.70137744648409e-07), ('Palate', 4.1274458783827483e-07), ('ah', 1.3679469198338023e-07), ('Background', 1.0105616800392044e-08), ('tut', 1.5051494781040819e-09), ('guh', 2.141249798003361e-10), ('oo', 1.4286215791111986e-10), ('ss', 4.582225804676413e-11), ('eh', 4.389796247229034e-11), ('t', 2.7894863984751273e-12), ('ay', 2.0826623620192393e-12), ('nn', 5.2838578398781345e-14), ('sh', 5.1482970562186956e-14), ('er', 1.1666032491015419e-14), ('yi', 2.2962451831459282e-17)])
# ----------------------
# parrot top classes: [('pop', 100.0), ('oh', 0.0), ('cough', 0.0)] pow=22.18
# items dict_items([('pop', 0.9999968744215149), ('Palate', 2.987982722857049e-06), ('Alveolar click', 8.720047688725434e-08), ('Background', 4.576483918598807e-08), ('cough', 4.377475612356303e-09), ('oh', 2.280992646900965e-10), ('guh', 1.5084840531553135e-11), ('ah', 8.08072779239093e-12), ('oo', 1.7034721155879365e-12), ('ay', 1.2700078645202348e-15), ('tut', 4.923681821431772e-16), ('ss', 2.9607097510422057e-16), ('t', 1.920933573766404e-17), ('er', 1.1624964301057098e-17), ('eh', 4.975767301140997e-18), ('nn', 2.535259587915452e-18), ('yi', 4.67345049679242e-19), ('sh', 4.468529232223396e-21)])
# items dict_items([('pop', 0.6002950262902209), ('guh', 0.3933931368974105), ('Palate', 0.005126113494063808), ('cough', 0.001001765232365727), ('Alveolar click', 6.553314211351191e-05), ('oh', 5.224955895769904e-05), ('oo', 3.8375675147734266e-05), ('Background', 1.8429741279898063e-05), ('ah', 7.342369675609689e-06), ('tut', 1.8716532920734538e-06), ('nn', 8.668463644443607e-08), ('ss', 4.71002157622007e-08), ('ay', 1.3160546362584252e-08), ('yi', 7.2427904559399005e-09), ('t', 1.522766218408751e-09), ('eh', 1.2760524353558971e-10), ('sh', 1.0099148723718312e-10), ('er', 5.9207414680411465e-12)])
# items dict_items([('guh', 0.7999430042891893), ('ss', 0.13646490747534493), ('yi', 0.0587545715662011), ('eh', 0.00302581997211526), ('ay', 0.0007791707651607046), ('sh', 0.0005363580167079692), ('oh', 0.0002164871253206818), ('oo', 0.00016823754485592064), ('cough', 7.685263148227931e-05), ('ah', 2.8470033535859023e-05), ('t', 5.605633917104689e-06), ('Palate', 2.510263718837254e-07), ('tut', 1.399162526797295e-07), ('nn', 1.1886765596626104e-07), ('er', 4.759508028400315e-09), ('pop', 3.7192214698905565e-10), ('Alveolar click', 3.050294298329478e-12), ('Background', 1.408069438588649e-12)])
# items dict_items([('pop', 0.9283376890606141), ('oh', 0.07088225556147715), ('ah', 0.0007654213483616936), ('cough', 9.084275788409565e-06), ('oo', 3.259656629590606e-06), ('Alveolar click', 9.801889372945836e-07), ('Palate', 6.949755904939782e-07), ('guh', 5.515154308824482e-07), ('Background', 3.337492393271298e-08), ('tut', 2.8954750073877363e-08), ('ay', 6.060208677211239e-10), ('sh', 2.798411994090609e-10), ('ss', 1.3957820198800258e-10), ('eh', 3.087956883330734e-11), ('yi', 2.157861796319889e-11), ('nn', 4.3043008773908204e-12), ('t', 4.257005902669285e-12), ('er', 1.0367039476735235e-12)])
# items dict_items([('pop', 0.999942123440016), ('Palate', 5.542432247144152e-05), ('Background', 2.0523821363178072e-06), ('Alveolar click', 1.387881059772238e-07), ('cough', 1.374287907808732e-07), ('oo', 6.684803317771211e-08), ('guh', 4.280390832567662e-08), ('oh', 1.3440362323385352e-08), ('ah', 5.421631610850661e-10), ('ay', 3.3229984357564436e-12), ('ss', 4.942482454483787e-13), ('tut', 8.986330137276393e-14), ('nn', 7.417712070243465e-14), ('t', 1.8830293895028953e-14), ('yi', 7.859900287739268e-15), ('er', 3.8909147653884894e-15), ('eh', 5.506562496872938e-16), ('sh', 2.365894813403582e-16)])
# ----------------------
# parrot top classes: [('pop', 99.99), ('Palate', 0.01), ('Background', 0.0)] pow=14.40
# items dict_items([('guh', 0.8968793990102153), ('pop', 0.10257070878075222), ('oo', 0.0003811950039509128), ('ah', 7.101741782327937e-05), ('Palate', 4.902331282002184e-05), ('oh', 3.383183184189418e-05), ('cough', 1.3869186722598067e-05), ('Background', 5.59909992246288e-07), ('Alveolar click', 2.395955188608008e-07), ('tut', 1.2219511661004826e-07), ('ss', 2.4102242518626184e-08), ('nn', 7.42322418225377e-09), ('t', 1.089318477922237e-09), ('ay', 6.952754292876201e-10), ('yi', 3.2049960732894105e-10), ('sh', 1.20080859348127e-10), ('eh', 2.463537404561049e-12), ('er', 2.141523017965097e-12)])
# items dict_items([('yi', 0.7953505092850941), ('ss', 0.16509505492546706), ('cough', 0.03943174961653719), ('ah', 3.753532346978895e-05), ('Palate', 1.9530939431233255e-05), ('ay', 1.7874094462156035e-05), ('t', 1.4843302827265901e-05), ('guh', 1.1119639994759306e-05), ('eh', 1.0660584100356371e-05), ('tut', 8.219721890081085e-06), ('sh', 1.3829314419363188e-06), ('Alveolar click', 9.018059849550967e-07), ('oo', 4.683741600516491e-07), ('Background', 6.854205064003573e-08), ('nn', 3.8840042664880434e-08), ('pop', 3.150473729336068e-08), ('oh', 9.566667554753588e-09), ('er', 1.001640960599653e-09)])
# items dict_items([('tut', 0.8555885940703041), ('guh', 0.07996410786787657), ('Background', 0.04453293180067547), ('Palate', 0.007079732757478463), ('pop', 0.0022950475689680616), ('cough', 0.0022488514905528874), ('eh', 0.002032040319083517), ('ss', 0.0017285250031749925), ('t', 0.0016742530187425116), ('ah', 0.0011400484870219333), ('sh', 0.0010288282464989626), ('nn', 0.0003237136536664169), ('yi', 0.00012535403788526157), ('ay', 6.596237818737149e-05), ('Alveolar click', 6.0913143656876526e-05), ('oo', 5.6586323302112326e-05), ('oh', 5.436449029648777e-05), ('er', 1.4534262802358707e-07)])
# items dict_items([('cough', 0.45614683174678694), ('tut', 0.3

        active: set[str] = set()
        for pattern in parrot_delegate.patterns.values():
            # if pattern.name == "pop":
                # pattern.get_throttles() {'pop': 0.15, 'ah': 0.1, 'eh': 0.15, 'oh': 0.1, 'oo': 0.15, 'guh': 0.15}
                # 1 ------------------ 1428105.1104308001 ----------------
                # OUT pattern.is_active(frame.ts) True
                # OUT frame.power 14.375865417734762
                # OUT frame.ts 1428105.1104308001
                # OUT top 3 frame.classes.items() [('cough', 0.9553141169423712), ('oh', 0.027970081532787294), ('guh', 0.013876626098384887)]
                # OUT detect(frame) False
                # OUT pattern.timestamps NoiseTimestamps(
                    # last_detected_at=0.0,
                    # duration_start=0.0,
                    # detection_after=0.0,
                    # graceperiod_until=0,
                    # throttled_at=0.0,
                    # throttled_until=0.0)
                # 2 ------------------ 1428105.1284038 ----------------
                # OUT pattern.is_active(frame.ts) True
                # OUT frame.power 18.7176749139649
                # OUT frame.ts 1428105.1284038
                # OUT top 3 frame.classes.items() [('pop', 0.9999004155709847), ('oh', 9.204145298130013e-05), ('cough', 3.9758382584555595e-06)]
                # OUT detect(frame) True
                # OUT pattern.timestamps NoiseTimestamps(
                    # last_detected_at=1428105.1284038,
                    # duration_start=1428105.1284038,
                    # detection_after=0.0,
                    # graceperiod_until=1428105.1284038,
                    # throttled_at=0.0,
                    # throttled_until=0.0)
                # 3 ------------------ 1428105.1464374 ----------------
                # OUT pattern.is_active(frame.ts) False
                # OUT frame.power 12.298429060623587
                # OUT frame.ts 1428105.1464374
                # OUT top 3 frame.classes.items() [('pop', 0.9999999104716559), ('Alveolar click', 6.046851758586652e-08), ('Palate', 2.050488837965456e-08)]
                # OUT detect(frame) False
                # OUT pattern.timestamps NoiseTimestamps(
                    # last_detected_at=1428105.1284038,
                    # duration_start=0,
                    # detection_after=0.0,
                    # graceperiod_until=0,
                    # throttled_at=1428105.1284038,
                    # throttled_until=1428105.2784038)
                # 4 ------------------ 1428105.1464374 ----------------
                # OUT pattern.is_active(frame.ts) False
                # OUT frame.power 2.776240470933892
                # OUT frame.ts 1428105.1464374
                # OUT top 3 frame.classes.items() [('pop', 0.8089588437351394), ('ah', 0.12546019778082154), ('oo', 0.034558506357845624)]
                # OUT detect(frame) False
                # OUT pattern.timestamps NoiseTimestamps(
                    # last_detected_at=1428105.1284038,
                    # duration_start=0,
                    # detection_after=0.0,
                    # graceperiod_until=0,
                    # throttled_at=1428105.1284038,
                    # throttled_until=1428105.2784038)
                # print(f"------------------ {frame.ts} ----------------")
                # print("OUT pattern.is_active(frame.ts)", pattern.is_active(frame.ts))
                # basically ALWAYS true - any noise has some power
                # print("OUT frame.power", frame.power)
                # print("OUT frame.ts", frame.ts)
                # print("OUT top 3 frame.classes.items()", sorted(frame.classes.items(), key=lambda x: x[1], reverse=True)[:3])
                # OUT top 3 frame.classes.items() [
                    # ('pop', 0.9999004155709847),
                    # ('oh', 9.204145298130013e-05),
                    # ('cough', 3.9758382584555595e-06)]
            detect = pattern.detect(frame)
            # if pattern.name == "pop":
                # print("OUT detect(frame)", detect)
                # OUT detect(frame) True
                # print("OUT pattern.timestamps", pattern.timestamps)
                # OUT pattern.timestamps NoiseTimestamps(
                    # last_detected_at=1428105.1284038,
                    # duration_start=1428105.1284038,
                    # detection_after=0.0,
                    # graceperiod_until=1428105.1284038,
                    # throttled_at=0.0,
                    # throttled_until=0.0)
            # if detect and pattern.name == "pop":
            #     print("parrot_delegate.patterns", parrot_delegate.patterns)
                # parrot_delegate.patterns {'ah': <user.roku_parrot_model.parrot_integration.NoisePattern object at 0x000002CB15B0D130>, 'cluck': <user.roku_parrot_model.parrot_integration.NoisePattern object at 0x000002CB15B0D3B0>, 'ee': <user.roku_parrot_model.parrot_integration.NoisePattern object at 0x000002CB15B0D6D0>, 'eh': <user.roku_parrot_model.parrot_integration.NoisePattern object at 0x000002CB15B0D810>, 'er': <user.roku_parrot_model.parrot_integration.NoisePattern object at 0x000002CB15B0DE50>, 'guh': <user.roku_parrot_model.parrot_integration.NoisePattern object at 0x000002CAB605A2B0>, 'hiss': <user.roku_parrot_model.parrot_integration.NoisePattern object at 0x000002CAB605A670>, 'nn': <user.roku_parrot_model.parrot_integration.NoisePattern object at 0x000002CAB60596D0>, 'oh': <user.roku_parrot_model.parrot_integration.NoisePattern object at 0x000002CAB60598B0>, 'palate_click': <user.roku_parrot_model.parrot_integration.NoisePattern object at 0x000002CAB6059950>, 'pop': <user.roku_parrot_model.parrot_integration.NoisePattern object at 0x000002CAB6059A90>, 'shush': <user.roku_parrot_model.parrot_integration.NoisePattern object at 0x000002CAB6059B30>, 'tut': <user.roku_parrot_model.parrot_integration.NoisePattern object at 0x000002CAB605B390>, 't': <user.roku_parrot_model.parrot_integration.NoisePattern object at 0x000002CAB6059DB0>}
                # print("parrot_delegate.last_frame_was_forwardpass", parrot_delegate.last_frame_was_forwardpass)
                # parrot_delegate.last_frame_was_forwardpass True
                # print("parrot_delegate.classes", parrot_delegate.classes)
                # parrot_delegate.classes {'nn', 'Background', 'cough', 'eh', 'yi', 't', 'oo', 'ss', 'pop', 'ah', 'ay', 'guh', 'tut', 'sh', 'er', 'Alveolar click', 'Palate', 'oh'}
                # print("parrot_delegate.raw_patterns", parrot_delegate.raw_patterns)
                # parrot_delegate.raw_patterns [<user.roku_parrot_model.parrot_integration.NoisePattern object at 0x000002CB15B0D130>, <user.roku_parrot_model.parrot_integration.NoisePattern object at 0x000002CB15B0D3B0>, <user.roku_parrot_model.parrot_integration.NoisePattern object at 0x000002CB15B0D6D0>, <user.roku_parrot_model.parrot_integration.NoisePattern object at 0x000002CB15B0D810>, <user.roku_parrot_model.parrot_integration.NoisePattern object at 0x000002CB15B0DE50>, <user.roku_parrot_model.parrot_integration.NoisePattern object at 0x000002CAB605A2B0>, <user.roku_parrot_model.parrot_integration.NoisePattern object at 0x000002CAB605A670>, <user.roku_parrot_model.parrot_integration.NoisePattern object at 0x000002CAB60596D0>, <user.roku_parrot_model.parrot_integration.NoisePattern object at 0x000002CAB60598B0>, <user.roku_parrot_model.parrot_integration.NoisePattern object at 0x000002CAB6059950>, <user.roku_parrot_model.parrot_integration.NoisePattern object at 0x000002CAB6059A90>, <user.roku_parrot_model.parrot_integration.NoisePattern object at 0x000002CAB6059B30>, <user.roku_parrot_model.parrot_integration.NoisePattern object at 0x000002CAB605B390>, <user.roku_parrot_model.parrot_integration.NoisePattern object at 0x000002CAB6059DB0>]
                # print("pattern.name", pattern.name)
                # pattern.name pop
                # print("pattern.timestamps", pattern.timestamps)
                # pattern.timestamps NoiseTimestamps(
                    # last_detected_at=1426520.8396164002,
                    # duration_start=1426520.8396164002,
                    # detection_after=0.0,
                    # graceperiod_until=1426520.8396164002,
                    # throttled_at=0.0,
                    # throttled_until=0.0)
                # print("pattern.labels", pattern.labels)
                # pattern.labels frozenset({'pop'})
                # print("pattern.duration", pattern.duration)
                # pattern.duration 0.0
                # print("pattern.detect(frame)", detect)
                # pattern.detect(frame) True
                # print("pattern.is_active(frame.ts)", pattern.is_active(frame.ts))
                # pattern.is_active(frame.ts) True
                # print("pattern.get_throttles()", pattern.get_throttles())
                # pattern.get_throttles() {'pop': 0.15, 'ah': 0.1, 'eh': 0.15, 'oh': 0.1, 'oo': 0.15, 'guh': 0.15}
                # print("frame.ts", frame.ts)
                # frame.ts 1426520.8396164002
                # print("frame.power", frame.power)
                # frame.power 39.933950936818874
                # print("frame.f0", frame.f0)
                # frame.f0 898.4927001837166
                # print("frame.f1", frame.f1)
                # frame.f1 902.213422530152
                # print("frame.f2", frame.f2)
                # frame.f2 1500.9914116803834
                # print("frame.classes.items()", frame.classes.items())
                # frame.classes.items() dict_items([
                    # ('pop', 0.9958910125246806),
                    # ('Alveolar click', 0.0040627052015612935),
                    # ('cough', 4.527995330714863e-05),
                    # ('ah', 4.015631081593758e-07), ('Palate', 3.8920934214307495e-07), ('Background', 1.3384880086858307e-07), ('tut', 4.071646983046745e-08), ('oh', 3.5903728732795296e-08), ('guh', 1.0277698407137148e-09), ('oo', 3.5015050106608664e-11), ('eh', 7.918394017877206e-12), ('ay', 6.53537260488096e-12), ('t', 1.371437144253744e-12), ('ss', 3.665947940944725e-13), ('er', 2.0899067816113937e-14), ('sh', 2.454768423369115e-15), ('yi', 1.11281544871009e-15), ('nn', 1.020983630896868e-16)])

            if detect:
                active.add(pattern.name)
                # print(f"active {pattern.name} {frame.ts} {frame.power:.2f} f0={frame.f0:.3f} f1={frame.f1:.3f} f2={frame.f2:.3f}")
                throttles = pattern.get_throttles()
                # print(f"throttles {throttles}")
                parrot_delegate.throttle_patterns(throttles, frame.ts)

        capture_collection.add(frame, active)

        # if active:
        #     # print("----------------------")
        #     # print(f"{len(active)} active patterns")
        #     # print("active", active)
        #     top_classes = sorted(frame.classes.items(), key=lambda item: item[1], reverse=True)
        #     # print('parrot', f"top classes: {[(k, round(v*100, 2)) for k, v in top_classes[:3]]} pow={frame.power:.2f}")
        #     # for pattern in parrot_delegate.patterns.values():
        #     #     if pattern.detect(frame):
        #     #         pattern.get_throttles()
        #     #         active.add(pattern.name)
        #     #         parrot_delegate.throttle_patterns(pattern.get_throttles(), frame.ts)

        #     top = sorted(frame.classes.items(), key=lambda item: item[1], reverse=True)
        #     if len(top) > 1:
        #         first, second = top[0], top[1]
        #         if second[1] > 0.6 * first[1]:  # tweak threshold as needed
        #             print(f"[SPY] Close call: {first[0]} ({first[1]:.2f}) vs {second[0]} ({second[1]:.2f})")
            # for a in active:
            #     winner_label, winner_prob = next(iter(frame.classes.items()))
            #     print('parrot', f"predict {winner_label} {winner_prob * 100:.2f}% pow={frame.power:.2f} f0={frame.f0:.3f} f1={frame.f1:.3f} f2={frame.f2:.3f}")
        return active
    return wrapper

original_pattern_match = None

def parrot_tester_wrap_parrot_integration(parrot_delegate, file: str):
    global original_pattern_match
    if original_pattern_match is None:
        with open(file, "r", encoding="utf-8") as f:
            print("Wrapping pattern_integration.py")
            original_pattern_match = parrot_delegate.pattern_match
            parrot_delegate.pattern_match = wrap_pattern_match(parrot_delegate)
            parrot_delegate.set_patterns(json.load(f))

def parrot_tester_restore_parrot_integration(parrot_delegate, original_file: str):
    """Restore pattern patterns."""
    global original_pattern_match
    if original_pattern_match is not None:
        parrot_delegate.pattern_match = original_pattern_match
        original_pattern_match = None

    with open(original_file, "r", encoding="utf-8") as f:
        parrot_delegate.set_patterns(json.load(f))
        print("Restored pattern_integration.py")

    reset_capture_collection()

def generate_parrot_integration_hook(import_path: str, current_file: Path):
    target_dir = current_file.parent.parent / "auto_generated"
    test_file = target_dir / "parrot_integration_hook.py"

    code = f"""\
# AUTO-GENERATED
try:
    from talon import Module
    from {import_path} import parrot_delegate
    from ..src.utils import (
        parrot_tester_wrap_parrot_integration,
        parrot_tester_restore_parrot_integration
    )

    mod = Module()

    @mod.action_class
    class Actions:
        def parrot_tester_wrap_parrot_integration(file: str):
            \"\"\"Wrap parrot_integration file\"\"\"
            parrot_tester_wrap_parrot_integration(parrot_delegate, file)

        def parrot_tester_restore_parrot_integration(original_file: str):
            \"\"\"Restore parrot_integration file\"\"\"
            parrot_tester_restore_parrot_integration(parrot_delegate, original_file)
except ImportError:
    pass
"""

    test_file.write_text(code)
    print(f"✅ Wrote test file to {test_file}")

def copy_patterns_to_generated(original_path: Path, generated_path: Path):
    generated_path = generated_path / "patterns_draft.json"
    try:
        with original_path.open("r", encoding="utf-8") as f:
            patterns = json.load(f)

        for pattern in patterns.values():
            for section in ("threshold", "grace_threshold"):
                if section in pattern:
                    if ">power" in pattern[section]:
                        pattern[section][">power"] = 1

        with generated_path.open("w", encoding="utf-8") as f:
            json.dump(patterns, f, indent=2)

        print(f"✅ Copied patterns.json to: {generated_path}")
        return patterns
    except Exception as e:
        print(f"❌ Failed to copy patterns.json: {e}")
        return {}

def create_auto_generated_folder(generated_folder: Path):
    """Create the auto_generated folder if it doesn't exist."""
    try:
        generated_folder.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created auto_generated folder: {generated_folder}")
    except Exception as e:
        print(f"❌ Failed to create auto_generated folder: {e}")

def generate_talon_noises_file(patterns: dict, generated_folder: Path):
    """Generate the talon_noises.py file based on the patterns."""
    target_file = generated_folder / "parrot_tester_active.talon"
    code = f"""# AUTO-GENERATED
tag: user.parrot_tester
not mode: sleep
-
<phrase>: skip()
parrot(pop):
    user.parrot_tester_discrete("pop", power, f0, f1, f2)
    mouse_click()
"""
    for name, config in patterns.items():
        if name == "pop":
            continue

        is_continuous = config.get("graceperiod", False)

        if is_continuous:
            code += f"parrot({name}): user.parrot_tester_continuous_start(\"{name}\", power, f0, f1, f2)\n"
            code += f"parrot({name}:stop): user.parrot_tester_continuous_stop(\"{name}\")\n"
        else:
            code += f"parrot({name}): user.parrot_tester_discrete(\"{name}\", power, f0, f1, f2)\n"

    target_file.write_text(code)
    print(f"✅ Wrote talon_noises.py to {target_file}")

def parrot_tester_initialize():
    """Test function to check if the paths are correct."""
    global patterns_json
    parrot_integration_path = get_parrot_integration_path().resolve()
    patterns_py_path = get_patterns_py_path().resolve()
    current_path = Path(__file__).resolve()
    generated_folder = Path(current_path.parent.parent / "auto_generated").resolve()

    current = Path(__file__).resolve()
    target = Path(parrot_integration_path).resolve()
    user_root = Path(TALON_USER).resolve()

    current_rel = current.relative_to(user_root)
    target_rel = target.relative_to(user_root).with_suffix("")  # drop .py

    patterns_json = load_patterns(patterns_py_path)

    # Example:
    # for name, config in patterns.items():
    #     print(f"{name}: {config}")

    print("TALON_USER:", TALON_USER)
    print("current_path:", current_path)
    print("parrot_integration_path:", parrot_integration_path)
    import_path = build_relative_import_path(current_rel, target_rel)
    print(import_path)
    create_auto_generated_folder(generated_folder)
    copy_patterns_to_generated(patterns_py_path, generated_folder)
    generate_talon_noises_file(patterns_json, generated_folder)
    generate_parrot_integration_hook(import_path, current_path)
    patterns_draft = Path(generated_folder / "patterns_draft.json").resolve()
    print(f"patterns_draft: {patterns_draft}")
    actions.user.parrot_tester_wrap_parrot_integration(patterns_draft)

    print(f"Parrot Integration Path: {parrot_integration_path}")
    print(f"Patterns.py Path: {patterns_py_path}")

def restore_patterns():
    """Restore the original patterns.json file."""
    original_path = get_patterns_py_path().resolve()
    actions.user.parrot_tester_restore_parrot_integration(original_path)