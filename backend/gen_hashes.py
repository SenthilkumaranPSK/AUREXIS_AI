from security import hash_password

users = [
    "SK@2000", "Imayavarman@2000", "Srivarshan@2000", "Rahulprasath@2000",
    "Magudesh@2000", "Deepak@2000", "Mani@2000", "Dineshkumar@2000",
    "Avinash@2000", "Kumar@2000", "Hari@2000", "Janakrishnan@2000"
]

for p in users:
    print(f"{p}: {hash_password(p)}")
