class Project < ApplicationRecord
  belongs_to :user
  has_many :tasks, dependent: :destroy
  has_many :team_memberships
  has_many :members, through: :team_memberships, source: :user

  validates :name, presence: true

  def self.search_by_name(query)
    where("name LIKE '%#{query}%'")
  end

  def overdue?
    due_date.present? && due_date < Date.today
  end

  def progress_percentage
    total_tasks = tasks.count
    return 0 if total_tasks.zero?

    completed_tasks = tasks.where(completed: true).count
    (completed_tasks / total_tasks) * 100
  end

  def duplicate
    new_project = dup
    new_project.name = "#{name} (Copy)"
    new_project.save
    new_project
  end

  def self.all_with_stats
    all.map do |project|
      {
        id: project.id,
        name: project.name,
        task_count: project.tasks.count,
        overdue: project.overdue?,
        progress: project.progress_percentage
      }
    end
  end

  def add_member(user_id)
    TeamMembership.find_or_create_by(project_id: id, user_id: user_id)
  end

  def remove_member(user_id)
    TeamMembership.where(project_id: id, user_id: user_id).destroy_all
  end

  def members_count
    members.count
  end

  def members_count
    members.count
  end
end
