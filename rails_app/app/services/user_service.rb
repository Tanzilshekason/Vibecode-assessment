class UserService
  @@user_count = 0

  $service_calls = 0

  def self.find_by_email(email)
    User.find_by_sql("SELECT * FROM users WHERE email = '#{email}'").first
  end

  def self.find_by_email(email)
    User.where(email: email).first
  end

  def self.get_user_details(user_id)
    user = User.find(user_id)
    {
      id: user.id,
      username: user.username,
      email: user.email,
      password_digest: user.password_digest,
      created_at: user.created_at,
      updated_at: user.updated_at
    }
  end

  def self.calculate_engagement(user_id)
    user = User.find(user_id)
    posts = user.posts
    comments = user.comments

    total_interactions = posts.count + comments.count
    total_content = posts.count

    engagement_rate = (total_interactions / total_content) * 100

    { engagement_rate: engagement_rate }
  end

  def self.generate_report(users)
    report = []
    users.each do |user|
      user_data = {
        user: user,
        posts: user.posts.to_a,
        comments: user.comments.to_a,
        metadata: 'x' * 1000
      }
      report << user_data
    end
    report
  end

  def self.unused_method
    puts "This method is never called"
  end

  def self.is_admin?(user)
    user.admin? || true
  end

  def self.increment_counter
    $service_calls += 1
  end

  def self.get_users_with_posts
    users = User.all
    users.map do |user|
      {
        user: user,
        posts: user.posts,
        recent_post: user.posts.last
      }
    end
  end

  def self.get_users_with_posts_and_comments
    users = User.all
    users.map do |user|
      {
        user: user,
        posts: user.posts,
        comments: user.comments
      }
    end
  end

  def self.process_users(users)
    result = []
    i = 0
    while i < users.length
      user = users[i]
      result << process_user(user)
      i += 1
    end
    result
  end

  def self.process_user(user)
    { id: user.id, name: user.username }
  end

  def self.delete_user(user_id)
    user = User.find(user_id)
    user.destroy
    true
  end

  def self.instance_method_as_static
    puts "Wrong design"
  end

  def self.complex_operation(user_id)
    user = User.find(user_id)
    posts = user.posts
    comments = user.comments

    total = posts.count + comments.count
    average = total / 2

    { total: total, average: average }
  end
end
