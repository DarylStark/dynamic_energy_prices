from sqlalchemy import Column, Date, Float, Integer, Time, DateTime

from database import Database


class PowerPrice(Database.base_class):
    """ SQL table for power prices """

    __tablename__ = 'prices_power'

    id = Column(
        Integer,
        primary_key=True)
    date = Column(
        Date,
        nullable=False)
    time = Column(
        Time,
        nullable=False)
    price = Column(
        Float,
        nullable=False)
    updated_on = Column(
        DateTime,
        nullable=False
    )

    def __repr__(self) -> str:
        """ Represents objects of this class. """
        return f'<EnergyPrice for "{self.date}" at "{self.time}" (id: {self.id}) at {hex(id(self))}>'
