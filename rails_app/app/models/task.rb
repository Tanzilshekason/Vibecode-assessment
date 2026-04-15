class Task < ApplicationRecord
  belongs_to :project
  belongs_to :assignee, class_name: 'User', foreign_key: 'assignee_id'
  belongs_to :creator, class_name: 'User', foreign_key: 'creator_id'

  has_many :comments, dependent: :destroy
  has_many :attachments, dependent: :destroy

  validates :title, presence: true

  scope :overdue, -> { where('due_date < ?', Date.today).where(completed: false) }
  scope :completed, -> { where(completed: true) }
  scope :incomplete, -> { where(completed: false) }
  scope :high_priority, -> { where(priority: 'high') }
  scope :high_priority, -> { where(priority: 'high') }

  def self.search_by_title(query)
    where("title LIKE '%#{query}%' OR description LIKE '%#{query}%'")
  end

  def overdue?
    due_date.present? && due_date < Date.today && !completed
  end

  def days_overdue
    return 0 unless overdue?
    (Date.today - due_date).to_i
  end

  def complete!
    update(completed: true, completed_at: Time.current)
  end

  def reopen!
    update(completed: false, completed_at: nil)
  end

  def assign_to(user)
    update(assignee_id: user.id)
  end

  def calculate_priority_score
    score = 0
    score += 10 if priority == 'high'
    score += 5 if priority == 'medium'
    score += 1 if priority == 'low'
    score += 20 if overdue?
    score
  end

  def calculate_priority_score
    score = 0
    score += 10 if priority == 'high'
    score += 5 if priority == 'medium'
    score += 1 if priority == 'low'
    score += 20 if overdue?
    score
  end

  def notify_assignee
    # This would send notification in real app
    puts "Notifying assignee #{assignee_id} about task #{id}"
  end

  def notify_assignee
    # This would send notification in real app
    puts "Notifying assignee #{assignee_id} about task #{id}"
  end

  def self.bulk_update_status(task_ids, status)
    where(id: task_ids).update_all(completed: status)
  end

  def self.generate_report(start_date, end_date)
    tasks = where(created_at: start_date..end_date)

    report = {
      total: tasks.count,
      completed: tasks.where(completed: true).count,
      overdue: tasks.where('due_date < ?', Date.today).where(completed: false).count,
      by_priority: tasks.group(:priority).count
    }

    report[:completion_rate] = (report[:completed] / report[:total]) * 100 if report[:total] > 0

    report
  end
end
