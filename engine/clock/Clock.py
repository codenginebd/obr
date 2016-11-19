import pytz
from datetime import datetime
import time
from django.utils import timezone

__author__ = 'codengine'

class Clock(object):
    @classmethod
    def timenow(cls):
        return datetime.now()

    @classmethod
    def timestampnow(cls):
        return int(datetime.now().strftime("%s"))

    @classmethod
    def convert_ts_to_datetime(cls, ts):
        return datetime.fromtimestamp(ts)

    @classmethod
    def convert_datetime_to_timestamp(cls,dt):
        return int(dt.strftime("%Y%m%d"))

    @classmethod
    def convert_datetime_to_utc_timestamp(cls,dt):
        return int(dt.strftime("%s"))

    @classmethod
    def timestampbefore(cls,hour):
        now_timestamp = Clock.timestampnow()
        sec = hour * 3600
        return now_timestamp - sec

    @classmethod
    def timestampahead(cls,hour):
        now_timestamp = Clock.timestampnow()
        sec = hour * 3600
        return now_timestamp + sec

    @classmethod
    def utc_now(cls): ###Make sure in settngs.py USE_TZ=True
        return datetime.utcnow()

    @classmethod
    def utc_timestamp(cls):
        return int(time.mktime(timezone.now().replace(tzinfo=None).timetuple())) #int(time.mktime(datetime.utcnow().timetuple()))

    @classmethod
    def utc_to_local_datetime(cls,dt,tz):
        local_tz = pytz.timezone(tz)
        utc_dt = pytz.utc.localize(dt)
        return utc_dt.astimezone(local_tz)

    @classmethod
    def convert_to_utc(cls,datestring,format='%d/%m/%Y'):
        dt = datetime.strptime(datestring,format)
        return time.mktime(dt.timetuple())

    @classmethod
    def convert_local_to_utc(cls,timezone,dt):
        tz = pytz.timezone (timezone) #"America/Los_Angeles"
        local_dt = tz.localize(dt, is_dst=None)
        utc_dt = local_dt.astimezone (pytz.utc)
        return utc_dt

    @classmethod
    def convert_utc_to_local(cls,timezone,dt):
        return cls.utc_to_local_datetime(dt,timezone)

    @classmethod
    def convert_local_to_utc_timestamp(cls,timezone,ts):
        dt = datetime.fromtimestamp(ts)
        tz = pytz.timezone (timezone) #"America/Los_Angeles"
        local_dt = tz.localize(dt, is_dst=None)
        utc_dt = local_dt.astimezone (pytz.utc)
        return time.mktime(utc_dt.timetuple())

    @classmethod
    def convert_utc_to_local_timestamp(cls,timezone,ts):
        local_dt = Clock.utc_to_local_datetime(datetime.fromtimestamp(int(ts)),timezone)
        return int(local_dt.strftime("%s"))

    @classmethod
    def get_all_timezones(cls, **kwargs):
        import pytz,math
        timezones = []
        input_utc_offset = kwargs.get("utc_offset")
        try:
            input_utc_offset = float(input_utc_offset)
        except:
            pass
        for tz in pytz.common_timezones:
            try:
                utc_offset = math.floor(pytz.timezone(tz)._utcoffset.total_seconds()/3600)
            except Exception as msg:
                td = pytz.timezone(tz)._utcoffset
                ts = (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6
                utc_offset = math.floor(ts/3600)
            utc_offset_temp = utc_offset
            if utc_offset >= 0:
                utc_offset = "+"+str(utc_offset)
            else:
                utc_offset = str(utc_offset)
            try:
                utc_offset = float(utc_offset)
            except:
                pass
            if input_utc_offset:
                if input_utc_offset == utc_offset:
                    temp_utc_offset =  str(utc_offset)
                    if utc_offset > 0:
                        if not "+" in temp_utc_offset:
                            temp_utc_offset = "+" + temp_utc_offset
                    else:
                        if not "-" in temp_utc_offset:
                            temp_utc_offset = "-" + temp_utc_offset
                    timezones += [(tz, "(UTC "+ temp_utc_offset + ") " + tz, utc_offset_temp)]
            else:
                temp_utc_offset =  str(utc_offset)
                if utc_offset > 0:
                    if not "+" in temp_utc_offset:
                        temp_utc_offset = "+" + temp_utc_offset
                else:
                    if not "-" in temp_utc_offset:
                        temp_utc_offset = "-" + temp_utc_offset

                timezones += [(tz, "(UTC "+temp_utc_offset + ") " + tz, utc_offset_temp)]

        timezones = sorted(timezones,key=lambda l: l[0])
        return timezones

    @classmethod
    def convert_seconds_to_hhmmss(cls,seconds):
        hours = seconds // (60*60)
        seconds %= (60*60)
        minutes = seconds // 60
        seconds %= 60
        return (hours, minutes, seconds,)

    """
    Right way to convert datetime.
    python datetime has an attribute tzinfo. By default datetime object is unaware of tzinfo. We have to
    assign a tzinfo to make it datetime aware.
    Say we want to convert a local time(Singapure) to UTC and then UTC back to that local.

    local_tz = "Asia/Singapure"  ##This is the local timezone

    tz_info = pytz.timezone(local_tz) ##Create a timezone object.

    job_start_datetime = tz_info.localize(job_start_datetime) ##Localize the datetime using tz object.

    utc_tz = pytz.utc  ##utc zone

    job_start_datetime = job_start_datetime.astimezone(utc_tz) ###convert local to utc

    lesson_timestamp = time.mktime(job_start_datetime.timetuple()) ###Convert datetime to timestamp

    dd = datetime.fromtimestamp(lesson_timestamp, tz=tz_info) ###Now convert utc timestamp back to local datetime. Provide a tzinfo object.

    """
    @classmethod
    def local_to_utc_datetime(cls, datetime_string, dt_format, tz):
        local_tz = tz
        local_tzinfo = pytz.timezone(local_tz)
        dt_time = datetime.strptime(datetime_string, dt_format)
        dt_time = local_tzinfo.localize(dt_time)

        utc_tz = pytz.utc
        dt_time = dt_time.astimezone(utc_tz)
        return dt_time

    @classmethod
    def utc_timestamp_to_local_datetime(cls, ts, tz):
        tz_info = pytz.timezone(tz)
        return datetime.fromtimestamp(ts, tz=tz_info)