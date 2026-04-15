class TasksController < ApplicationController
  before_action :set_task, only: [:show, :edit, :update, :destroy, :complete, :reopen]
  skip_before_action :verify_authenticity_token, only: [:create, :update, :destroy]

  def index
    if params[:project_id]
      @tasks = Task.where(project_id: params[:project_id])
    else
      @tasks = Task.all
    end

    if params[:status] == 'completed'
      @tasks = @tasks.completed
    elsif params[:status] == 'incomplete'
      @tasks = @tasks.incomplete
    elsif params[:status] == 'overdue'
      @tasks = @tasks.overdue
    end

    if params[:search]
      @tasks = @tasks.search_by_title(params[:search])
    end

    @tasks = @tasks.order(created_at: :desc)

    respond_to do |format|
      format.html
      format.json { render json: @tasks }
    end
  end

  def show
    @comments = @task.comments
    @attachments = @task.attachments

    respond_to do |format|
      format.html
      format.json { render json: { task: @task, comments: @comments, attachments: @attachments } }
    end
  end

  def new
    @task = Task.new
    @task.project_id = params[:project_id] if params[:project_id]
  end

  def edit
  end

  def create
    @task = Task.new(task_params)
    @task.creator_id = current_user.id if current_user

    if @task.save
      redirect_to @task, notice: 'Task was successfully created.'
    else
      render :new
    end
  end

  def update
    if @task.update(task_params)
      redirect_to @task, notice: 'Task was successfully updated.'
    else
      render :edit
    end
  end

  def destroy
    @task.destroy
    redirect_to tasks_url, notice: 'Task was successfully destroyed.'
  end

  def complete
    @task.complete!
    redirect_to @task, notice: 'Task marked as completed.'
  end

  def reopen
    @task.reopen!
    redirect_to @task, notice: 'Task reopened.'
  end

  def bulk_update
    task_ids = params[:task_ids]
    status = params[:status] == 'true'

    Task.bulk_update_status(task_ids, status)

    redirect_to tasks_url, notice: 'Tasks updated successfully.'
  end

  def assign
    @task = Task.find(params[:id])
    user = User.find(params[:user_id])

    @task.assign_to(user)
    @task.notify_assignee

    redirect_to @task, notice: 'Task assigned successfully.'
  end

  def report
    start_date = params[:start_date] ? Date.parse(params[:start_date]) : 30.days.ago.to_date
    end_date = params[:end_date] ? Date.parse(params[:end_date]) : Date.today

    @report = Task.generate_report(start_date, end_date)

    respond_to do |format|
      format.html
      format.json { render json: @report }
    end
  end

  def overdue
    @tasks = Task.overdue

    respond_to do |format|
      format.html
      format.json { render json: @tasks }
    end
  end

  private

  def set_task
    @task = Task.find(params[:id])
  end

  def task_params
    params.require(:task).permit(:title, :description, :due_date, :priority, :project_id, :assignee_id)
  end
end
