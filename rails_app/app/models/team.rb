class Team < ApplicationRecord
  has_many :team_memberships, dependent: :destroy
  has_many :members, through: :team_memberships, source: :user
  has_many :projects

  validates :name, presence: true

  def add_member(user, role = 'member')
    TeamMembership.find_or_create_by(team_id: id, user_id: user.id, role: role)
  end

  def remove_member(user)
    TeamMembership.where(team_id: id, user_id: user.id).destroy_all
  end

  def is_member?(user)
    members.include?(user)
  end

  def is_member?(user)
    members.include?(user)
  end

  def member_count
    members.count
  end

  def project_count
    projects.count
  end

  def active_projects
    projects.where(status: 'active')
  end

  def completed_projects
    projects.where(status: 'completed')
  end

  def self.search(query)
    where("name LIKE '%#{query}%' OR description LIKE '%#{query}%'")
  end

  def generate_performance_report
    total_projects = projects.count
    completed_projects = projects.where(status: 'completed').count
    active_projects = projects.where(status: 'active').count

    completion_rate = total_projects > 0 ? (completed_projects / total_projects) * 100 : 0

    {
      team_id: id,
      team_name: name,
      total_projects: total_projects,
      completed_projects: completed_projects,
      active_projects: active_projects,
      completion_rate: completion_rate,
      member_count: member_count
    }
  end

  def duplicate
    new_team = dup
    new_team.name = "#{name} (Copy)"
    new_team.save

    members.each do |member|
      new_team.add_member(member)
    end

    new_team
  end

  def archive
    update(archived: true, archived_at: Time.current)
  end

  def unarchive
    update(archived: false, archived_at: nil)
  end
end
