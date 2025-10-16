from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    DateTime,
    Float,
    func,
)
from sqlalchemy.orm import relationship
from app.database import Base


# ===============================================================
# 🧑 USER MODEL
# ===============================================================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(120), unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String(50), nullable=False)  # CIVILIAN, PROSECUTOR, JUDGE, REGISTRAR

    # Relationships
    filed_cases = relationship(
        "Case",
        back_populates="created_by",
        foreign_keys="Case.created_by_id",
        cascade="all, delete-orphan",
    )
    assigned_cases = relationship(
        "Case",
        back_populates="assigned_to",
        foreign_keys="Case.assigned_to_id",
    )
    evidences = relationship(
        "Evidence",
        back_populates="uploaded_by",
        cascade="all, delete-orphan",
    )
    hearings_as_judge = relationship(
        "Hearing",
        back_populates="judge",
        foreign_keys="Hearing.judge_id",
    )
    hearings_as_registrar = relationship(
        "Hearing",
        back_populates="registrar",
        foreign_keys="Hearing.registrar_id",
    )


# ===============================================================
# ⚖️ CASE MODEL
# ===============================================================
class Case(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(100), default="Filed")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Foreign keys
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    assigned_to_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Relationships
    created_by = relationship(
        "User",
        back_populates="filed_cases",
        foreign_keys=[created_by_id],
    )
    assigned_to = relationship(
        "User",
        back_populates="assigned_cases",
        foreign_keys=[assigned_to_id],
    )
    notes = relationship(
        "CaseNote",
        back_populates="case",
        cascade="all, delete-orphan",
    )
    evidences = relationship(
        "Evidence",
        back_populates="case",
        cascade="all, delete-orphan",
    )
    hearings = relationship(
        "Hearing",
        back_populates="case",
        cascade="all, delete-orphan",
    )
    payments = relationship(
        "Payment",
        back_populates="case",
        cascade="all, delete-orphan",
    )


# ===============================================================
# 📝 CASE NOTE MODEL
# ===============================================================
class CaseNote(Base):
    __tablename__ = "case_notes"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    note = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    case = relationship("Case", back_populates="notes")
    author = relationship("User")


# ===============================================================
# 📁 EVIDENCE MODEL
# ===============================================================
class Evidence(Base):
    __tablename__ = "evidence"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    filetype = Column(String(50), nullable=False)
    filepath = Column(String(500), nullable=True)
    uploaded_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    case = relationship("Case", back_populates="evidences")
    uploaded_by = relationship("User", back_populates="evidences")


# ===============================================================
# 🗓️ HEARING MODEL
# ===============================================================
class Hearing(Base):
    __tablename__ = "hearings"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False)
    registrar_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    judge_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    scheduled_date = Column(DateTime, nullable=False)
    location = Column(String(255), nullable=False)
    notes = Column(Text, nullable=True)
    status = Column(String(100), default="Scheduled")

    # Relationships
    case = relationship("Case", back_populates="hearings")
    registrar = relationship("User", foreign_keys=[registrar_id], back_populates="hearings_as_registrar")
    judge = relationship("User", foreign_keys=[judge_id], back_populates="hearings_as_judge")


# ===============================================================
# 💳 PAYMENT MODEL
# ===============================================================
class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False)
    payer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    payment_type = Column(String(50), nullable=False)
    reference = Column(String(120), nullable=True)
    status = Column(String(50), default="Pending")  # Pending, Completed, Failed
    date = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    case = relationship("Case", back_populates="payments")
    payer = relationship("User")

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    uploader_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False)
    file_type = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    upload_date = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    uploader = relationship("User")
    case = relationship("Case")