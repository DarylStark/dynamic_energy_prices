from sqlalchemy import Column, Date, Float, Integer, Time, DateTime

from database import Database


class GasPrice(Database.base_class):
    """ SQL table for gas prices """

    __tablename__ = 'prices_gas'

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
        return f'<GasPrice for "{self.date}" at "{self.time}" [{self.price:.2f}] (id: {self.id}) at {hex(id(self))}>'
