# def signal_glue(self, portion_x1, portion_y1, portion_x2, portion_y2, order):
#     portion_x1 = portion_x1.tolist()
#     portion_x2 = portion_x2.tolist()
#     portion_y1 = portion_y1.tolist()
#     portion_y2 = portion_y2.tolist()
#
#     interp_y_func = lambda arguments: None
#     x_interp = []
#     total_range = (abs(portion_x1[-1] - portion_x1[0])) + (abs(portion_x2[-1] - portion_x2[0]))
#
#     print("signal 1 came first")
#     print(portion_x1[0], portion_x2[0])
#
#     if portion_x1[0] < portion_x2[0]:
#         print("signal 1 el as8ar")
#         gap = self.gap_or_overlap(total_range, portion_x1[0], portion_x2[-1])
#         if gap:
#             x_list = portion_x1 + portion_x2
#             y_list = portion_y1 + portion_y2
#             x_interp = np.linspace(portion_x1[-1] + 1e-6,
#                                    portion_x2[0] - 1e-6)  # Make sure to use a consistent size
#             interp_y_func = interp1d(x_list, y_list, kind=order)
#             y_interp = interp_y_func(x_interp)
#
#             # Use np.concatenate to ensure correct concatenation
#             self.glued_x = np.concatenate([portion_x1, x_interp, portion_x2])
#             self.glued_y = np.concatenate([portion_y1, y_interp, portion_y2])
#             return self.glued_x, self.glued_y
#         else:
#             intersection = list(set(portion_x1) & set(portion_x2))
#             x_list = portion_x1[:-len(intersection)] + portion_x2[len(intersection):]
#             y_list = portion_y1[:-len(intersection)] + portion_y2[len(intersection):]
#             x_interp = np.linspace(portion_x2[0] + 1e-6,
#                                    portion_x1[-1] - 1e-6)  # Make sure to use a consistent size
#             interp_y_func = interp1d(x_list, y_list, kind=order)
#             y_interp = interp_y_func(x_interp)
#
#             self.glued_x = np.concatenate(
#                 [portion_x1[:-len(intersection)], x_interp, portion_x2[len(intersection):]])
#             self.glued_y = np.concatenate(
#                 [portion_y1[:-len(intersection)], y_interp, portion_y2[len(intersection):]])
#
#             print(self.glued_x)
#             return self.glued_x, self.glued_y
#
#     elif portion_x2[0] < portion_x1[0]:
#         print("signal 2 el as8ar")
#         gap = self.gap_or_overlap(total_range, portion_x2[0], portion_x1[-1])
#         if gap:
#             x_list = portion_x2 + portion_x1
#             y_list = portion_y2 + portion_y1
#             x_interp = np.linspace(portion_x2[-1] + 1e-6, portion_x1[0] - 1e-6, num=100)
#             interp_y_func = interp1d(x_list, y_list, kind=order)
#             y_interp = interp_y_func(x_interp)
#
#             self.glued_x = np.concatenate([portion_x2, x_interp, portion_x1])
#             self.glued_y = np.concatenate([portion_y2, y_interp, portion_y1])
#             return self.glued_x, self.glued_y
#         else:
#             intersection = list(set(portion_x1) & set(portion_x2))
#             x_list = portion_x2[:-len(intersection)] + portion_x1[len(intersection):]
#             y_list = portion_y2[:-len(intersection)] + portion_y1[len(intersection):]
#             x_interp = np.linspace(portion_x1[0] + 1e-6,
#                                    portion_x2[-1] - 1e-6)  # Make sure to use a consistent size
#             interp_y_func = interp1d(x_list, y_list, kind=order)
#             y_interp = interp_y_func(x_interp)
#
#             self.glued_x = np.concatenate(
#                 [portion_x1[:-len(intersection)], x_interp, portion_x2[len(intersection):]])
#             self.glued_y = np.concatenate(
#                 [portion_y1[:-len(intersection)], y_interp, portion_y2[len(intersection):]])
#
#             print(self.glued_x)
#             return self.glued_x, self.glued_y


# x = [1, 2, 3, 4, 5, 6, 6.2, 7,7.1, 7.4, 8, 8.5, 9]
# y = [6, 7, 7.8, 8, 9, 10, 11, 12]
#
# # Find the first intersection point (the minimum element in the intersection)
# intersection = set(x) & set(y)
# first_intersection = min(intersection, key=lambda val: x.index(val))
#
# # Get values from x starting from the first intersection
# x_start = x[x.index(first_intersection):]
#
# # Get values from y until the first intersection
# y_until = [val for val in y if val <= first_intersection]
#
# # Combine the lists, removing duplicates
# overlapping_elements = x_start + [val for val in y_until if val not in x_start]
#
# # Sort the overlapping elements (optional)
# overlapping_elements_sorted = sorted(overlapping_elements)
#
# print(overlapping_elements_sorted)


x = [1, 2, 3, 4, 5, 6, 6.2, 7, 7.1, 7.4, 8, 8.5, 9]
y = [6, 7, 7.8, 8, 9, 10, 11, 12]

# Find the first intersection point (the minimum element in the intersection)
intersection = set(x) & set(y)
print(intersection)

# Initialize the indices
initial_index = 0
final_index = 0

# Find the index of the first intersection point in x
for i, val in enumerate(x):
    if val == min(intersection):  # Using min to get the smallest intersection point
        initial_index = i
        break

# Find the index of the last intersection point in y
for i, val in enumerate(y):
    if val == max(intersection):  # Using max to get the largest intersection point
        final_index = i
        break

# Combine the parts of the lists
x_list = set(x[initial_index:] + y[:final_index])
print(sorted(x_list))
print(initial_index, final_index)

