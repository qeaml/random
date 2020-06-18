def get_timedelta_tuple(d):
	days, t = divmod(d.total_seconds(), 24 * 60 ** 2)
	hours, t = divmod(t, 60 ** 2)
	minutes, t = divmod(t, 60)
	seconds = t
	return days, hours, minutes, seconds
	
if __name__ == '__main__':
	from datetime import timedelta
	
	delta = timedelta(hours=49, minutes=13, seconds=44)
	d, h, m, s = get_timedelta_tuple(delta)
	
	print(f"The timedelta holds these values: {d} days {h} hours {m} minutes and {s} seconds.")
