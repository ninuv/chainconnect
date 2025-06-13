

av_languages = ['eng', 'deu', 'ser']


translations = {
    'deu': {
        'Feed': 'Startseite',
        'Following': 'Gefolgt',
        'Search': 'Suche',
        'Search People': 'Suche Leute',
        'Followers': 'Follower',
        'Edit Profile': 'Profil Bearbeiten',
        'Share what you think...': 'Du hast {{ current_user.followers.count() }} Freunde, {{ current_user.fullname }}. Du solltest ihnen etwas posten...',
        'Post': 'Posten',
        'Profile': 'Profil',
        'Follow': 'Folgen',
        'Unfollow': 'Gefolgt',
        'Logout': 'Ausloggen',
        'Name': 'Name',
        'Username': 'Benutzername',
        'Pronouns': 'Pronomen',
        'E-Mail': 'E-Mail',
        'Bio': 'Beschreibung',
        'Your Bio': 'Beschreibe Dich!',
        'Suspend Profile': 'Sus Profil',
        'Delete Profile': 'Profil Löschen',
        'Save': 'Speichern',
        'Back': 'Zurück',
        'Write a comment...': 'Schreibe einen Kommentar...',
        'Cancel': 'Abbrechen',
        'Comment': 'Kommentieren',
        'Likes': 'Likes',
        'Settings': 'Einstellungen',

        'Share': 'Teilen',
        'Block User': 'Benutzer Blockieren',
        'Unblock User': 'Nicht Mehr Blockieren',
        'Report User': 'Benutzer Melden',

        'Change Language': 'Sprache ändern',
        'English': 'Englisch',
        'German': 'Deutsch',
        'Swedish': 'Schwedisch',
        'Serenic': 'Serenisch',

        # translations that will become irrelevant
        'Home': 'Start',
        'Search': 'Suche',
        'Create': 'Schreibe',
        'Notes': 'Neues',
        'del': 'löschen'
    },
    'eng': {
        'Feed': 'Feed',
        'Following': 'Following',
        'Search': 'Search',
        'Search People': 'Search People',
        'Followers': 'Followers',
        'Edit Profile': 'Edit Profile',
        'Share what you think...': 'Share what you think...',
        'Post': 'Post',
        'Profile': 'Profile',
        'Follow': 'Follow',
        'Unfollow': 'Unfollow',
        'Logout': 'Logout',
        'Name': 'Name',
        'Username': 'Username',
        'Pronouns': 'Pronouns',
        'E-Mail': 'E-Mail',
        'Bio': 'Bio',
        'Your Bio': 'Your Bio',
        'Suspend Profile': 'Suspend Profile',
        'Delete Profile': 'Delete Profile',
        'Save': 'Save',
        'Back': 'Back',
        'Change Language': 'Change Language',
        'Write a comment...': 'Write a comment...',
        'Cancel': 'Cancel',
        'Comment': 'Comment',
        'Likes': 'Likes',
        'Settings': 'Settings',

        'Share': 'Share',
        'Block User': 'Block User',
        'Unblock User': 'Unblock User',
        'Report User': 'Report User',

        'English': 'English',
        'German': 'German',
        'Swedish': 'Swedish',
        'Serenic': 'Serenic',

        # translations that will become irrelevant
        'Home': 'Home',
        'Search': 'Search',
        'Create': 'Create',
        'Notes': 'Notes',
        'del': 'del'
    },
    'ser': {
        'Feed': 'Aregin',
        'Following': 'Casas',
        'Search': 'Tusila',
        'Search People': 'Tusile Lurier',
        'Followers': 'Case Eire',
        'Edit Profile': 'Sergana Vanu',
        'Share what you think...': 'Ey ludagen durus...',
        'Post': 'Merana',
        'Profile': 'Vanu',
        'Follow': 'Casa',
        'Unfollow': 'Casina',
        'Logout': 'Lerasin',
        'Name': 'Tinei',
        'Username': 'Ilatinei',
        'Pronouns': 'Len-tineir',
        'E-Mail': 'Corenas',
        'Bio': 'Dareis',
        'Your Bio': 'Dareis Ginas',
        'Suspend Profile': 'Iyema Vanu',
        'Delete Profile': 'Sedana Vanu',
        'Save': 'Argonis',
        'Back': 'Ternis',
        'Change Language': 'Gurka Telis',
        'Write a comment...': 'Merana Terkun...',
        'Cancel': 'Ternis',
        'Comment': 'Terkun',
        'Likes': 'Gulina',
        'Settings': 'Gurka',

        'Share': 'Lureis',
        'Block User': 'Terna Vanu',
        'Unblock User': 'Ternina Vanu',
        'Report User': 'Surkira Vanu',

        'English': 'Ernelin',
        'German': 'Cermanin',
        'Swedish': 'Suyedin',
        'Serenic': 'Serenin',

        # translations that will become irrelevant
        'Home': 'Arivan',
        'Search': 'Tusila',
        'Create': 'Merana',
        'Notes': 'Argonis',
        'del': 'lina'
    }
}


def t(key, lang='eng'):
    return translations.get(lang, {}).get(key, key)