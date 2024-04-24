from flask import Blueprint, jsonify, make_response
from . import db_session
from .feedbacks import Feedback


blueprint = Blueprint(
    'feedbacks_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/feedbacks', methods=['GET', 'POST'])
def get_feedbacks():
    db_sess = db_session.create_session()
    feedbacks = db_sess.query(Feedback).all()
    return jsonify(
        {
            'feedbacks':
                [item.to_dict(only=('text', 'date', 'user.full_name'))
                 for item in feedbacks]
        }
    )


@blueprint.route('/api/feedbacks/<int:feedbacks_id>', methods=['GET'])
def get_one_feedback(feedbacks_id):
    db_sess = db_session.create_session()
    news = db_sess.query(Feedback).get(feedbacks_id)
    if not news:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'feedback': news.to_dict(only=(
                'text', 'date', 'user_id', 'user.full_name'))
        }
    )