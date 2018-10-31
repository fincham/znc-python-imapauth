import imaplib

import znc

class catalystauth(znc.Module):
    description = "Python IMAP authentication"
    module_types = [znc.CModInfo.GlobalModule]

    def OnLoginAttempt(self, auth):
        username = auth.GetUsername()
        password = auth.GetPassword()
        imap_username = "%s@example.com" % username
        connection = imaplib.IMAP4_SSL("mail.example.com")
        try:
            connection.login(imap_username, password)
        except Exception as e:
            auth.RefuseLogin("Catalyst authentication failed")
            return znc.HALT
        else:
            connection.logout()

        user = znc.CZNC.Get().FindUser(username)
        if user is None:
            template_user = znc.CZNC.Get().FindUser("template")
            new_user = znc.CUser(username)
            str_err = znc.String()
            new_user.Clone(template_user, str_err)
            new_user.SetNick(username)
            new_user.SetAltNick(username)
            new_user.SetIdent(username)
            if znc.CZNC.Get().AddUser(new_user, str_err):
                new_user.thisown = 0
                auth.AcceptLogin(new_user)
        else:
            auth.AcceptLogin(user)

        return znc.HALT
