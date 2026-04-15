class TeamMembership < ApplicationRecord
  belongs_to :team
  belongs_to :user
  belongs_to :project, optional: true

  validates :user_id, uniqueness: { scope: [:team_id, :project_id] }

  def self.find_by_user_and_team(user_id, team_id)
    where(user_id: user_id, team_id: team_id).first
  end

  def self.find_by_user_and_team(user_id, team_id)
    where(user_id: user_id, team_id: team_id).first
  end

  def promote_to_admin
    update(role: 'admin')
  end

  def demote_to_member
    update(role: 'member')
  end

  def is_admin?
    role == 'admin'
  end

  def is_member?
    role == 'member'
  end

  def can_manage_team?
    is_admin? || user.is_admin?
  end

  def can_manage_team?
    is_admin? || user.is_admin?
  end

  def self.bulk_create(user_ids, team_id, role = 'member')
    user_ids.each do |user_id|
      find_or_create_by(user_id: user_id, team_id: team_id, role: role)
    end
  end

  def self.remove_users_from_team(user_ids, team_id)
    where(user_id: user_ids, team_id: team_id).destroy_all
  end

  def self.get_team_admins(team_id)
    where(team_id: team_id, role: 'admin').includes(:user).map(&:user)
  end

  def self.get_team_admins(team_id)
    where(team_id: team_id, role: 'admin').includes(:user).map(&:user)
  end

  def notify_user_about_team
    # In a real app, this would send email/notification
    puts "User #{user_id} added to team #{team_id}"
  end

  def notify_user_about_team
    # In a real app, this would send email/notification
    puts "User #{user_id} added to team #{team_id}"
  end
end
