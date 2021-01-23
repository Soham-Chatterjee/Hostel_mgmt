from passlib.hash import pbkdf2_sha256
import pickle

with open("pvt.dat", "wb") as f_in:
    password = "admin"
    hashed_pass = pbkdf2_sha256.hash(password)
    pickle.dump(hashed_pass, f_in)


with open("pvt.dat", "rb") as pvt_file:
    pswd_correct = pickle.load(pvt_file)
