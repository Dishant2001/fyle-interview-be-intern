from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment

from .schema import AssignmentSchema, AssignmentSubmitSchema
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)


@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.auth_principal
def list_assignments(p):
    """Returns list of assignments"""
    teacher_assignments = Assignment.get_assignments_for_teacher(p.teacher_id)
    teacher_assignments_dump = AssignmentSchema().dump(teacher_assignments, many=True)
    return APIResponse.respond(data=teacher_assignments_dump)



@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.auth_principal
def grade_assignment(p, incoming_payload):
    """Grade an assignment"""
    print("Entered grading")
    print(incoming_payload['id'])
    grade_assignment_payload = AssignmentSchema().load(incoming_payload)
    print(grade_assignment_payload.id,grade_assignment_payload.grade,'  ')
    graded_assignment = Assignment.grading(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        principal=p
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)
