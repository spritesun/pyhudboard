import os

def save_claims(claims):
    file_content = ''
    for build, person in claims.iteritems():
        if build and person:
            file_content += build + "::::" + person + "\n"
    f = open("peopleworkingonbuilds.txt.tmp", "w")
    f.write(file_content)
    f.close()
    os.rename("peopleworkingonbuilds.txt.tmp", "peopleworkingonbuilds.txt")

def get_claims_as_hash():
    claims = {}
    try:
        f = open("peopleworkingonbuilds.txt", 'r')
        lines = f.readlines()
        if len(lines) == 0:
            return {}
        for line in lines:
            try:
                build, person = line.split("::::")
                claims[build.strip()] = person.strip()
            except:
                #not a valid line apparently
                pass
    except IOError:
        pass
    return claims
