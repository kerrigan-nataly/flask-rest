import flask
from . import db_session
from .jobs import Jobs
from flask import jsonify, request

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('job', 'team_leader', 'work_size', 'collaborators', 'start_date', 'end_date',
                                    'is_finished'))
                 for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_one_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'job': job.to_dict(only=(
                'job', 'team_leader', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished'))
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'job', 'team_leader', 'collaborators', 'work_size', 'start_date', 'end_date',
                  'is_finished']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    check = db_sess.query(Jobs).filter(Jobs.id == request.json.get('id')).first()

    if check:
        return jsonify({'error': 'Id already exists'})

    job = Jobs(
        id=request.json.get('id'),
        job=request.json.get('job'),
        team_leader=request.json.get('team_leader'),
        collaborators=request.json.get('collaborators'),
        work_size=request.json.get('work_size'),
        start_date=request.json.get('start_date'),
        end_date=request.json.get('end_date'),
        is_finished=request.json.get('is_finished')
    )
    db_sess.add(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})
    db_sess.query(Jobs).filter(Jobs.id == job_id).update({
        Jobs.job: request.json.get('job'),
        Jobs.team_leader: request.json.get('team_leader'),
        Jobs.collaborators: request.json.get('collaborators'),
        Jobs.work_size: request.json.get('work_size'),
        Jobs.start_date: request.json.get('start_date'),
        Jobs.end_date: request.json.get('end_date'),
        Jobs.is_finished: request.json.get('is_finished')
    })
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})
    db_sess.delete(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})
