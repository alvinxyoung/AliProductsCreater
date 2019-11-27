from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker

engine=create_engine('sqlite:///C:\\Users\\Admin\\AliProductsCreater\\products.db')
Base=declarative_base()
Session=sessionmaker(bind=engine)

class Product(Base):
    __tablename__ = 'products'
    id=Column(Integer, autoincrement=True, primary_key=True)
    date_ = Column(DateTime(), nullable=False)
    catalog_id=Column(Integer(), nullable=False)
    product_id = Column(Integer, nullable=False)
    title=Column(String(128), nullable=False)
    main_img1=Column(String(), nullable=False)
    main_img2 = Column(String())
    main_img3 = Column(String())
    main_img4 = Column(String())
    main_img5 = Column(String())
    main_img6 = Column(String())
    propertyValueDisplayName=Column(String(),nullable=False) #skuPropertyName : propertyValueDisplayName sku 价格，属性，数量
    properties = Column(String()) #属性
    detail_img1=Column(String, nullable=False)
    detail_img2=Column(String)
    detail_img3 = Column(String)
    detail_img4 = Column(String)
    detail_img5 = Column(String)


Base.metadata.create_all(engine)