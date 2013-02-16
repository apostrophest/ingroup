from sqlalchemy.sql.expression import desc

from models import Applicant
from users import user_loader

def get_applicants(session):
    return session.query(Applicant).order_by(desc(Applicant.id)).all()

def get_prospective_applicants(session):
    return session.query(Applicant).filter(Applicant.processor_id == None).all()

def create_applicant(session, user, reason):
    applicant = Applicant(user, reason)
    session.add(applicant)
    return applicant


def accept_applicant(session, applicant_id, accepter):
    applicant = session.query(Applicant).filter(Applicant.id==applicant_id).first()
    if applicant:
        applicant.user.approved = True
        applicant.approved = True
        applicant.processor = accepter

    # TODO: send email to applicant

def reject_applicant(session, applicant_id, rejecter):
    applicant = session.query(Applicant).filter(Applicant.id==applicant_id).first()
    if applicant:
        user = user_loader(applicant.user_id)
        applicant.approved = False
        applicant.processor = rejecter
        applicant.user = None
        session.delete(user)

    # TODO: sent email to applicant