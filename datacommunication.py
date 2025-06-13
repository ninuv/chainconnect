import random
from models import Protocol, Notification


event = {
    'eng': {
        'RXXLK': ['User registered', ' registered on the app'],
        'LXXOK': ['User logs in', ' logged in'],
        'LXXIK': ['User logs out', ' logged out'],
        'DXXLK': ['User deleted account', ' deleted their account'],
        'DXXOK': ['User\'s account was deleted', '\'s account was deleted'],
        'CXXNK': ['User changed username', ' changed their username to'],
    },
    'deu': {
        'RXXLK': ['Benutzer registriert', ' hat sich registriert'],
        'LXXOK': ['Benutzer hat sich eingeloggt', ' hat sich eingeloggt'],
        'LXXIK': ['Benutzer hat sich ausgeloggt', ' hat sich ausgeloggt'],
        'DXXLK': ['Benutzer hat Account gelöscht', ' hat den eigenen Account gelöscht'],
        'DXXOK': ['Benutzer-Account wurde gelöscht', 's Account wurde gelöscht'],
        'CXXNK': ['Benutzer hat Benutzernamen geändert', ' änderte Benutzernamen zu'],
    },
    'ser': {
        'RXXLK': ['Runeres vanu rin', '- runeres rin'],
        'LXXOK': ['Sinuleres vanu', '- sinuleres'],
        'LXXIK': ['Lerasineres vanu', '- lerasineres'],
        'DXXLK': ['Lineres vanu', '- lineres'],
        'DXXOK': ['Lineres erge vanu', '- lineres vanures'],
        'CXXNK': ['Gurkeres vanu ilatinei', '- gurkeres ilatinei co'],
    }
}

note_event = {
    'eng': {
        'LYYTR': ['User received like', ' liked your *post~'],
        'CYYTR': ['User received comment', ' commented on your *post~'],
        'FYYTR': ['User received follow', ' follows you now'],
        'SYYTR': ['User\'s account suspended', 'Your account got suspended'],
        'SYYUR': ['User\'s account not suspended anymore', 'Your account is no longer suspended']
    },
    'deu': {
        'LYYTR': ['Benutzer bekam Like', ' gefällt dein *Post~'],
        'CYYTR': ['Benutzer bekam Kommentar', ' hat deinen *Post~ kommentiert'],
        'FYYTR': ['Benutzer bekam Follow', ' folgt dir jetzt'],
        'SYYTR': ['Benutzerkonto suspendiert', 'Dein Account wurde suspendiert'],
        'SYYUR': ['Benutzerkonto nicht mehr suspendiert', 'Dein Account ist nicht mehr suspendiert']
    },
    'ser': {
        'LYYTR': ['Tarunes vanu gulina', ', gulines *sa~ ginar'],
        'CYYTR': ['Tarunes vanu terkun', ', meraneres terkun co *sa~ ginar'],
        'FYYTR': ['Tarunes vanu casa', ', cases gire'],
        'SYYTR': ['Iyema erge vanu', 'Iyemes erge vanu ginar'],
        'SYYUR': ['Iyemina erge vanu', 'Iyemines erge vanu ginar']
    }
}


def write_protocol(user, event_id):
    ID = 'P-' + str(random.randint(100000, 999999))
    user_id = user.id
    user_name = user.username
    protocol = Protocol(id=ID, user_id=user_id, event_id=event_id, user_name=user_name)
    return protocol

def create_notification(receiving_user, toggle_user, event_id, post_id='', comment_id=''):
    ID = 'N-' + str(random.randint(100000, 999999))
    receiving_user_id = receiving_user.id
    toggle_user_id = toggle_user.id
    if post_id == '' and comment_id == '':
        notification = Notification(id=ID, receiving_user_id=receiving_user_id, toggle_user_id=toggle_user_id, event_id=event_id)
    elif post_id == '' and comment_id != '':
        notification = Notification(id=ID, receiving_user_id=receiving_user_id, toggle_user_id=toggle_user_id, event_id=event_id, comment_id=comment_id)
    elif post_id != '' and comment_id == '':
        notification = Notification(id=ID, receiving_user_id=receiving_user_id, toggle_user_id=toggle_user_id, event_id=event_id, post_id=post_id)
    elif post_id != '' and comment_id != '':
        notification = Notification(id=ID, receiving_user_id=receiving_user_id, toggle_user_id=toggle_user_id, event_id=event_id, comment_id=comment_id, post_id=post_id)
    return notification
