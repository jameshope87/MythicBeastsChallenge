from equationsolver import *
import smtplib
import srvlookup


def getPassword(url):
    eqn, secret = getEquation(getSoup(url))
    sols = solveEquation(eqn)
    soup = BeautifulSoup(submitForm(sols, secret),"html.parser")
#    print(soup)
    password = soup.tt.next_sibling[soup.tt.next_sibling.find("password")+9:-1]
#    print(password)
    return(password)

def sendMail():
    server = smtplib.SMTP('mail.jobs.mythic-beasts.com', srvlookup.lookup("submission", "tcp", "jobs.mythic-beasts.com")[0].port)
    server.login('step-3@jobs.mythic-beasts.com',getPassword(url))
    msg = "Hello"
    server.sendmail("step-3@jobs.mythic-beasts.com","james.hope87@gmail.com",msg)
    server.quit()

if __name__ == "__main__":
    sendMail()
