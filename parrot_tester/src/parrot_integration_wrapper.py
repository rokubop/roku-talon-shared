# from talon.experimental.parrot import ParrotFrame

# def wrap_pattern_match(pattern_match: callable):
#     def wrapper(frame: ParrotFrame):
#         winner_label, winner_prob = next(iter(frame.classes.items()))
#         print('parrot', f"predict {winner_label} {winner_prob * 100:.2f}% pow={frame.power:.2f} f0={frame.f0:.3f} f1={frame.f1:.3f} f2={frame.f2:.3f}")
#         return pattern_match(frame)
#     return wrapper

# class ParrotIntegrationHook:
#     def __init__(self, parrot):
#         self.parrot_integration_path = get_parrot_integration_path()
#         self.original_pattern_match = None

#     def patch(self, pattern_match: callable):
#         def wrapper(frame: ParrotFrame):
#             winner_label, winner_prob = next(iter(frame.classes.items()))
#             print('parrot', f"predict {winner_label} {winner_prob * 100:.2f}% pow={frame.power:.2f} f0={frame.f0:.3f} f1={frame.f1:.3f} f2={frame.f2:.3f}")
#             return pattern_match(frame)
#         return wrapper

# parrot_integration_hook = ParrotIntegrationHook()