INSERT INTO user (name, password)
VALUES
  ('test', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'),
  ('other', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79');

INSERT INTO food_type (food_type)
VALUES
  ('Pasta'), ('Grains'), ('Salad'), ('Breakfast');

INSERT INTO recipe (name, description, type_id)
VALUES
  ('Mac cheese', 'A tasty dish', 1),
  ('Fried Rice', 'Yummy', 2),
  ('Wild rice and greens', 'Healthy', 2),
  ('Caesar Salad', 'Refreshing!', 3);
