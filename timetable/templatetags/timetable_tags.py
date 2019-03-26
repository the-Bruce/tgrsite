from django import template

register = template.Library()


@register.filter
def for_event(weeks, event):
    result = []
    oldBookingTxt = bookingTxt = None
    run = 1
    for week in weeks:
        try:
            bookingTxt = week.booking_set.filter(event=event)[0].room
        except IndexError:
            bookingTxt = None

        if bookingTxt == oldBookingTxt:
            run += 1
        else:
            result.append((run, oldBookingTxt))
            run = 1
            oldBookingTxt = bookingTxt
    if bookingTxt == oldBookingTxt:
        result.append((run, oldBookingTxt))
    return result[1:]
