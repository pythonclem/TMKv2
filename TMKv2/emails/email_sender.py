from .get_email_data import usersAndTeams, generateEmailData 
from .email_renderer import generateHTML 
from .mailjet import sendEmail

def sendEmails():
    usersandteams = usersAndTeams()
    for user in usersandteams:
        emaildata = generateEmailData(user, usersandteams)
        generateHTML(emaildata['matches'], emaildata['userinfo']['name'], emaildata['userteams'])
        sendEmail(emaildata['userinfo']['email'])