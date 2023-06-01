import dateutil.parser

from src.base.table_base import TableBase


def main():
    dt = dateutil.parser.parse("2023-04-05 20:50:07.136630")
    dtf = TableBase.float_to_datetime(0)
    print(dtf)
    dtv = TableBase.datetime_to_float(dt)
    print(dtv)


if __name__ == '__main__':
    main()

