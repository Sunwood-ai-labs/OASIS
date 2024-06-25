class Post:
    def __init__(self, title, content, slug, categories, tags):
        self.title = title
        self.content = content
        self.slug = slug
        self.categories = categories
        self.tags = tags

    def to_dict(self):
        return {
            "title": self.title,
            "slug": self.slug,
            "categories": self.categories,
            "tags": self.tags
        }
