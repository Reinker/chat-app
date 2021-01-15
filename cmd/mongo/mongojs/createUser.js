const adminuser = {
  user: 'root',
  pwd: 'root',
  roles: [{
    role: 'root',
    db: 'admin'
  }]
};

db.createUser(adminuser);

const appuser = {
	user: 'chatapp',
	pwd: 'chatapp',
	roles: [{
		role: 'readWrite',
		db: 'chatapp'
	}]
}
db.createUser(appuser);
