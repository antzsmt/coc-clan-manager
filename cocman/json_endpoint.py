"""Defines the JSON API endpoints."""
from flask import jsonify
from sqlalchemy.orm.exc import NoResultFound

from cocman import app
from cocman.database_setup import Clan, Member
from cocman.connect_to_database import connect_to_database

@app.route('/clandata/mainclan/JSON/')
@app.route('/clandata/<clan_tag>/JSON/')
def clandata_json(clan_tag=None):
    """Returns data about the clan and its members in JSON format.

    Args:
        clan_tag (str): Clan tag that specifies the clan to be looked up. Note
            that the '#' symbol needs to be '%23' in the URL string.

    Returns:
        json_output (str): Clan and member data in JSON format.
    """
    if clan_tag is None:
        clan_tag = app.config['MAIN_CLAN_TAG']

    session = connect_to_database()

    try:
        clan = session.query(Clan).filter_by(tag=clan_tag).one()
    except NoResultFound:
        session.close()
        error_msg = 'Clan with tag ' + clan_tag + ' not found!'
        return jsonify(status=501, error=error_msg)

    json_output = jsonify(clan.serialise, status=200)
    session.close()
    return json_output
