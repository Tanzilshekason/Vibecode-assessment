Rails.application.routes.draw do
  get '/home', to: 'home#index'
  get '/home', to: 'home#index'
  get '/home', to: 'home#index'

  get '/unused', to: 'unused#index'

  get '/users/:id', to: 'users#show'
  get '/users/:id/edit', to: 'users#edit'
  post '/users/:id/update', to: 'users#update'

  resources :posts do
    resources :comments do
      resources :likes do
        resources :replies do
        end
      end
    end
  end

  # Task Management System routes
  resources :projects do
    member do
      post :add_member
      delete :remove_member
      get :stats
      get :export
    end
    resources :tasks, only: [:index, :new, :create]
  end

  resources :tasks, except: [:index, :new, :create] do
    member do
      post :complete
      post :assign
      get :report
    end
    collection do
      get :overdue
      get :search
    end
  end

  resources :teams do
    member do
      post :add_member
      delete :remove_member
      post :archive
      get :performance
    end
  end

  get '/search', to: 'search#query'

  get '/config', to: 'config#show'

  match '*path', to: 'errors#not_found', via: :all

  root 'home#index'
  root 'home#index'
end
