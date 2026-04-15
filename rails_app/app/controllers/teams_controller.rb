class TeamsController < ApplicationController
  before_action :set_team, only: [:show, :edit, :update, :destroy, :add_member, :remove_member, :archive, :unarchive]
  skip_before_action :verify_authenticity_token, only: [:create, :update, :destroy]

  def index
    if params[:search]
      @teams = Team.search(params[:search])
    else
      @teams = Team.all
    end

    @teams = @teams.order(created_at: :desc)

    respond_to do |format|
      format.html
      format.json { render json: @teams }
    end
  end

  def show
    @members = @team.members
    @projects = @team.projects

    respond_to do |format|
      format.html
      format.json { render json: { team: @team, members: @members, projects: @projects } }
    end
  end

  def new
    @team = Team.new
  end

  def edit
  end

  def create
    @team = Team.new(team_params)

    if @team.save
      redirect_to @team, notice: 'Team was successfully created.'
    else
      render :new
    end
  end

  def update
    if @team.update(team_params)
      redirect_to @team, notice: 'Team was successfully updated.'
    else
      render :edit
    end
  end

  def destroy
    @team.destroy
    redirect_to teams_url, notice: 'Team was successfully destroyed.'
  end

  def add_member
    user = User.find(params[:user_id])
    role = params[:role] || 'member'

    @team.add_member(user, role)

    redirect_to @team, notice: 'Member added successfully.'
  end

  def remove_member
    user = User.find(params[:user_id])
    @team.remove_member(user)

    redirect_to @team, notice: 'Member removed successfully.'
  end

  def archive
    @team.archive
    redirect_to @team, notice: 'Team archived successfully.'
  end

  def unarchive
    @team.unarchive
    redirect_to @team, notice: 'Team unarchived successfully.'
  end

  def duplicate
    @team = Team.find(params[:id])
    new_team = @team.duplicate

    redirect_to new_team, notice: 'Team duplicated successfully.'
  end

  def performance
    @teams = Team.all
    @performance_reports = @teams.map(&:generate_performance_report)

    respond_to do |format|
      format.html
      format.json { render json: @performance_reports }
    end
  end

  def bulk_add_members
    @team = Team.find(params[:id])
    user_ids = params[:user_ids]

    TeamMembership.bulk_create(user_ids, @team.id)

    redirect_to @team, notice: 'Members added successfully.'
  end

  def export_members
    @team = Team.find(params[:id])
    csv_data = CSV.generate do |csv|
      csv << ['User ID', 'Name', 'Email', 'Role']
      @team.team_memberships.includes(:user).each do |membership|
        user = membership.user
        csv << [user.id, user.name, user.email, membership.role]
      end
    end

    send_data csv_data, filename: "team-#{@team.id}-members-#{Date.today}.csv"
  end

  private

  def set_team
    @team = Team.find(params[:id])
  end

  def team_params
    params.require(:team).permit(:name, :description)
  end
end
