from math import ceil


def main():
    start_year = 0
    while start_year != -1:
        start_year, end_year = map(int, input("Enter range of years to check (eg. 2016 2017): ").split())
        print(f"Checking between {start_year} and {end_year}...")

        years_div_4 = div_years_in_range(start_year, end_year, 4)

        years_div_100 = div_years_in_range(start_year, end_year, 100)

        years_div_900_r_200 = div_years_in_range(max(0, start_year-200), end_year - 200, 900)
        years_div_900_r_600 = div_years_in_range(max(0, start_year - 600), end_year - 600, 900)

        leap_year_count = years_div_4 - years_div_100 + years_div_900_r_200 + years_div_900_r_600
        print(f"leap years: {leap_year_count}")


def div_years_in_range(start, end, d):
    next_div = start if (start % d == 0) else start + (d - start % d)
    return ceil((end - next_div) / (d*1.0)) if (next_div < end) else 0


if __name__ == "__main__":
    main()
