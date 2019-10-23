import math
import statistics

# Random Number Generator -- (Part 3)
def get_random_number(seed):
    x_i = seed     # seed
    a = 24693      # multiplier
    c = 3967       # increment
    K = 2**15      # modulus, 2^15

    x_i = ((a * x_i) + c) % K
    u_i = x_i / K

    return x_i, round(u_i, 4)


# Random Variable Generator for X (number of seconds to pick up the phone when available) -- (Part 4)
def generate_x_realization(random_number):
    x_i = -12 * math.log(1 - random_number)
    return round(x_i, 4)


# Random Variable Generator for W (Number of seconds spent calling a single customer)
def generate_w_realization(x_i):
    calling = True
    w = 0
    times_called = 0
    temp_random = get_random_number(x_i)[1]
    temp_random_x_i = get_random_number(x_i)[0]

    while calling and times_called < 4:     # Exits loop if customer picks up or doesn't answer 4 times in a row
        w += 6                                   # Takes 6 seconds to pick up the call
        times_called += 1                        # Keeps track of number of times the customer has been called
        if temp_random < 0.2:               # Busy signal
            w += 3                                  # 3 seconds to recognize busy signal and one to hang up
            w += 1
        elif 0.2 < temp_random < 0.5:       # Customer unavailable
            w += 25                                 # 25 seconds to wait for 5 rings and one to hang up
            w += 1
        else:                               # Customer is available (with probability 0.5)
            random_u = get_random_number(temp_random_x_i)[1]        # Get a random number between 0 and 1
            x_realization = generate_x_realization(random_u)        # Generate an X realization of this number (# secs)
            if x_realization < 25:                                  # If the number of seconds is less than 25:
                w += x_realization                                          # Then add that realization number to w
                calling = False                                             # And end the calling process
            else:
                w += 25                                             # Otherwise, the caller waits 25 seconds
                w += 1                                              # Then hangs up
        temp_random = get_random_number(temp_random_x_i)[1]         # Get the next random u value for calling process
        temp_random_x_i = get_random_number(temp_random_x_i)[0]     # Get the next random x value for the RNG

    return round(w, 4), temp_random_x_i                             # Return the W realization and x for RNG for next W


def generate_w_realizations(number):
    w_realizations = []                                             # Create a list to store W realizations
    random_number_x_i = get_random_number(1000)[0]                  # Gets 1st x value (x_1) for Random Number Generator

    for i in range(number):                                             # Run loop 1000 times
        w_realization = generate_w_realization(random_number_x_i)[0]            # Get the w_realization from above
        random_number_x_i = generate_w_realization(random_number_x_i)[1]        # Get the next x_i for RNG
        w_realizations.append(w_realization)

    return w_realizations


w_output = generate_w_realizations(1000)


lt_15 = 0
lt_20 = 0
lt_30 = 0
gt_40 = 0
sum = 0
for w in w_output:
    sum += w
    if w <= 15:
        lt_15 += 1
    if w <= 20:
        lt_20 += 1
    if w <= 30:
        lt_30 += 1
    if w > 40:
        gt_40 += 1

prob_lt_15 = lt_15 / 1000
prob_lt_20 = lt_20 / 1000
prob_lt_30 = lt_30 / 1000
prob_gt_40 = gt_40 / 1000
mean = round(statistics.mean(w_output), 4)
median = round(statistics.median(w_output), 4)

print("P[W <= 15] = " + str(prob_lt_15))
print("P[W <= 20] = " + str(prob_lt_20))
print("P[W <= 30] = " + str(prob_lt_30))
print("P[W > 40] = " + str(prob_gt_40))
print("Mean = " + str(mean))
print("Median = " + str(median))

w_sorted = sorted(w_output)

w_first = []
for i in range(0, 500):
    w_first.append(w_sorted[i])

w_second = []
for j in range(500, 1000):
    w_second.append(w_sorted[j])

first_quartile = round(statistics.median(w_first), 4)
third_quartile = round(statistics.median(w_second), 4)
print("First Quartile = " + str(first_quartile))
print("Third Quartile = " + str(third_quartile))


