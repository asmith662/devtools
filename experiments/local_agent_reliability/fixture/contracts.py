"""Public room-occupancy contract.

Reservations and the window are half-open numeric intervals. Count time once
even when reservations overlap; clip to the observation window. Ignore empty
or reversed reservations. Empty/reversed windows have zero occupied duration.
Input order is irrelevant. Do not mutate either input. Finite integer and
fractional numeric endpoints are supported; callers validate endpoint types.
"""
