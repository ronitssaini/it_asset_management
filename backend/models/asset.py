from sqlalchemy import Column, Integer, String, Date, Text
from backend.database.session import Base

class Asset(Base):
    __tablename__ = "assets"
    __table_args__ = {'extend_existing': True}

    # Unique Identifier
    serial_number = Column(String(50), primary_key=True, unique=True)

    # Common Fields (across all device types)
    company_name = Column(String(100), nullable=False)
    device_type = Column(String(50), nullable=False)  # e.g., Server, Switch, Desktop
    make = Column(String(50))
    os_version = Column(String(50))
    ip_address = Column(String(50))
    subnet_mask = Column(String(50))
    purchase_date = Column(Date)
    additional_device = Column(String(100))
    remarks = Column(Text)
    location = Column(String(100))

    # New: Store last 3 users for desktops/laptops as JSON string
    last_users = Column(Text)  # JSON-encoded list of last 3 users

    # Server-specific Fields
    typer = Column(String(50))                    # Physical / Virtual
    processor_type = Column(String(50))           # e.g., Intel
    processor = Column(String(50))                # Count or model
    total_processor_core = Column(Integer)
    internal_hard_disk = Column(String(50))       # e.g., 460GB
    disk_type = Column(String(50))                # e.g., SSD
    qty = Column(Integer)
    raid = Column(String(10))
    ram = Column(String(20))
    network_card = Column(String(100))            # e.g., 2-10G
    hba_card = Column(String(100))                # e.g., 2-32GB

    # Switch-specific Fields
    model = Column(String(100))
    no_of_ports = Column(Integer)

    # Desktop-specific Fields
    processor = Column(String(50))                # e.g., Intel i5
    ram = Column(String(20))                      # e.g., 8GB
    hard_disk = Column(String(50))                # e.g., 500GB HDD
    monitor = Column(String(100))
    employee_code = Column(String(50))            # Changed from emp_code
    employee_name = Column(String(100))
    function = Column(String(100))
    role = Column(String(100))

    # Storage-specific Fields
    model = Column(String(100))
    total_capacity = Column(String(50))
    # disk_type already exists
