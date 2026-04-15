class ProjectsController < ApplicationController
  before_action :set_project, only: [:show, :edit, :update, :destroy, :add_member, :remove_member]
  skip_before_action :verify_authenticity_token, only: [:create, :update, :destroy]

  def index
    if params[:search]
      @projects = Project.search_by_name(params[:search])
    else
      @projects = Project.all
    end

    @projects = @projects.order(created_at: :desc)

    respond_to do |format|
      format.html
      format.json { render json: @projects }
    end
  end

  def show
    @tasks = @project.tasks
    @members = @project.members

    respond_to do |format|
      format.html
      format.json { render json: { project: @project, tasks: @tasks, members: @members } }
    end
  end

  def new
    @project = Project.new
  end

  def edit
  end

  def create
    @project = Project.new(project_params)
    @project.user_id = current_user.id if current_user

    if @project.save
      redirect_to @project, notice: 'Project was successfully created.'
    else
      render :new
    end
  end

  def update
    if @project.update(project_params)
      redirect_to @project, notice: 'Project was successfully updated.'
    else
      render :edit
    end
  end

  def destroy
    @project.destroy
    redirect_to projects_url, notice: 'Project was successfully destroyed.'
  end

  def stats
    @projects = Project.all
    @total_projects = @projects.count
    @overdue_projects = @projects.select(&:overdue?).count
    @avg_progress = @projects.sum(&:progress_percentage) / @total_projects if @total_projects > 0

    render json: {
      total_projects: @total_projects,
      overdue_projects: @overdue_projects,
      average_progress: @avg_progress
    }
  end

  def add_member
    user = User.find(params[:user_id])
    @project.add_member(user.id)

    redirect_to @project, notice: 'Member added successfully.'
  end

  def remove_member
    @project.remove_member(params[:user_id])

    redirect_to @project, notice: 'Member removed successfully.'
  end

  def duplicate
    @project = Project.find(params[:id])
    new_project = @project.duplicate

    redirect_to new_project, notice: 'Project duplicated successfully.'
  end

  def export
    @projects = Project.all
    csv_data = CSV.generate do |csv|
      csv << ['ID', 'Name', 'Due Date', 'Progress', 'Overdue']
      @projects.each do |project|
        csv << [project.id, project.name, project.due_date, project.progress_percentage, project.overdue?]
      end
    end

    send_data csv_data, filename: "projects-#{Date.today}.csv"
  end

  private

  def set_project
    @project = Project.find(params[:id])
  end

  def project_params
    params.require(:project).permit(:name, :description, :due_date, :status)
  end
end
