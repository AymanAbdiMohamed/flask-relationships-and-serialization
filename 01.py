# to_dict() method

def to_dict(self):
    return {
        'name': self.name,
        'age': self.age,
        'email': self.email
    }

# serialization rules dictionary
serialize_rules = {
    'to_dict': to_dict
}
serialize_rules = ('-posts.user')
# when  serializing a user, include their posts
# but when serializing posts, exclude the user field to avoid circular reference
 

# cascading delete rules dictionary
cascade = "all, delete-orphan"
# if a user is deleted, delete all their posts automatically
# do not leave posts in the db with no owner

