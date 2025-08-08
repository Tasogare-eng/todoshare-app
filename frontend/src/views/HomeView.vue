<template>
  <div class="min-h-screen bg-white">
    <!-- Navigation -->
    <nav class="fixed top-0 w-full z-50 bg-white/95 backdrop-blur-xl border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <!-- Logo -->
          <div class="flex items-center">
            <div class="flex items-center">
              <div class="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center mr-3">
                <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              <span class="text-xl font-bold text-gray-900">TodoShare</span>
            </div>
          </div>

          <!-- Navigation Links -->
          <div class="hidden md:flex items-center space-x-8">
            <a href="#features" class="text-gray-600 hover:text-gray-900 text-sm font-medium">Features</a>
            <a href="#pricing" class="text-gray-600 hover:text-gray-900 text-sm font-medium">Pricing</a>
            <a href="#" class="text-gray-600 hover:text-gray-900 text-sm font-medium">About</a>
            <a href="#" class="text-gray-600 hover:text-gray-900 text-sm font-medium">Blog</a>
          </div>

          <!-- Auth Buttons -->
          <div class="flex items-center space-x-4">
            <router-link to="/login" class="text-gray-600 hover:text-gray-900 text-sm font-medium">Sign in</router-link>
            <router-link 
              to="/register" 
              class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
            >
              Get started
            </router-link>
          </div>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <section class="pt-24 pb-12 px-4 sm:px-6 lg:px-8">
      <div class="max-w-7xl mx-auto">
        <div class="text-center">
          <h1 class="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold text-gray-900 mb-6">
            Organize your team's work, 
            <span class="text-indigo-600">from start to finish</span>
          </h1>
          <p class="text-xl text-gray-600 max-w-3xl mx-auto mb-10 leading-relaxed">
            TodoShare is the productivity platform teams use to stay organized, 
            collaborate effectively, and deliver exceptional results.
          </p>
          
          <div class="flex flex-col sm:flex-row justify-center gap-4 mb-12">
            <router-link 
              to="/register" 
              class="bg-indigo-600 hover:bg-indigo-700 text-white px-8 py-4 rounded-xl text-lg font-semibold transition-colors shadow-lg"
            >
              Start building for free
            </router-link>
            <button class="flex items-center justify-center px-8 py-4 border border-gray-300 rounded-xl text-lg font-semibold text-gray-700 hover:bg-gray-50 transition-colors">
              <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
                <path d="M8 5v14l11-7z"/>
              </svg>
              Watch demo
            </button>
          </div>
          
          <p class="text-sm text-gray-500">
            ✓ Free forever • ✓ No credit card required • ✓ Setup in 2 minutes
          </p>
        </div>

        <!-- Hero Image -->
        <div class="mt-16 relative">
          <div class="bg-gradient-to-r from-indigo-50 to-blue-50 rounded-2xl p-8 border border-gray-200">
            <div class="bg-white rounded-xl shadow-2xl overflow-hidden">
              <!-- Mock Browser Bar -->
              <div class="bg-gray-50 px-4 py-3 border-b border-gray-200 flex items-center">
                <div class="flex space-x-2">
                  <div class="w-3 h-3 bg-red-400 rounded-full"></div>
                  <div class="w-3 h-3 bg-yellow-400 rounded-full"></div>
                  <div class="w-3 h-3 bg-green-400 rounded-full"></div>
                </div>
                <div class="flex-1 text-center">
                  <div class="bg-gray-200 rounded-full px-3 py-1 text-xs text-gray-600 inline-block">
                    app.todoshare.com
                  </div>
                </div>
              </div>
              
              <!-- Mock App Content -->
              <div class="p-6 bg-white">
                <div class="flex items-center justify-between mb-6">
                  <h3 class="text-lg font-semibold text-gray-900">Project Dashboard</h3>
                  <div class="flex items-center space-x-2">
                    <div class="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs font-medium">
                      On track
                    </div>
                    <button class="bg-indigo-600 text-white px-3 py-1 rounded-lg text-sm font-medium">
                      New task
                    </button>
                  </div>
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <!-- To Do Column -->
                  <div>
                    <h4 class="text-sm font-medium text-gray-500 uppercase tracking-wider mb-3">
                      To Do (3)
                    </h4>
                    <div class="space-y-3">
                      <div class="bg-gray-50 p-3 rounded-lg border border-gray-200">
                        <div class="flex items-start justify-between">
                          <div class="flex-1">
                            <h5 class="text-sm font-medium text-gray-900">Design new landing page</h5>
                            <p class="text-xs text-gray-500 mt-1">Due tomorrow</p>
                          </div>
                          <div class="w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center text-white text-xs font-medium">
                            A
                          </div>
                        </div>
                      </div>
                      
                      <div class="bg-gray-50 p-3 rounded-lg border border-gray-200">
                        <div class="flex items-start justify-between">
                          <div class="flex-1">
                            <h5 class="text-sm font-medium text-gray-900">Update user documentation</h5>
                            <p class="text-xs text-gray-500 mt-1">Due in 3 days</p>
                          </div>
                          <div class="w-6 h-6 bg-green-500 rounded-full flex items-center justify-center text-white text-xs font-medium">
                            M
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <!-- In Progress Column -->
                  <div>
                    <h4 class="text-sm font-medium text-gray-500 uppercase tracking-wider mb-3">
                      In Progress (2)
                    </h4>
                    <div class="space-y-3">
                      <div class="bg-yellow-50 p-3 rounded-lg border border-yellow-200">
                        <div class="flex items-start justify-between">
                          <div class="flex-1">
                            <h5 class="text-sm font-medium text-gray-900">API integration</h5>
                            <p class="text-xs text-gray-500 mt-1">Started 2 hours ago</p>
                          </div>
                          <div class="w-6 h-6 bg-purple-500 rounded-full flex items-center justify-center text-white text-xs font-medium">
                            S
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <!-- Done Column -->
                  <div>
                    <h4 class="text-sm font-medium text-gray-500 uppercase tracking-wider mb-3">
                      Done (5)
                    </h4>
                    <div class="space-y-3">
                      <div class="bg-green-50 p-3 rounded-lg border border-green-200">
                        <div class="flex items-start justify-between">
                          <div class="flex-1">
                            <h5 class="text-sm font-medium text-gray-900">Setup project repository</h5>
                            <p class="text-xs text-gray-500 mt-1">Completed yesterday</p>
                          </div>
                          <div class="w-6 h-6 bg-gray-400 rounded-full flex items-center justify-center text-white text-xs font-medium">
                            J
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Social Proof -->
    <section class="py-12 bg-gray-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <p class="text-center text-sm text-gray-600 mb-8">
          Trusted by teams at world-class companies
        </p>
        <div class="flex items-center justify-center space-x-12 grayscale opacity-60">
          <div class="text-2xl font-bold">Microsoft</div>
          <div class="text-2xl font-bold">Shopify</div>
          <div class="text-2xl font-bold">Stripe</div>
          <div class="text-2xl font-bold">Netflix</div>
          <div class="text-2xl font-bold">Airbnb</div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="py-24 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-20">
          <h2 class="text-4xl font-bold text-gray-900 mb-4">
            Everything your team needs to succeed
          </h2>
          <p class="text-xl text-gray-600 max-w-3xl mx-auto">
            From project planning to execution, TodoShare provides all the tools 
            you need to keep your team aligned and productive.
          </p>
        </div>

        <div class="grid lg:grid-cols-3 gap-8">
          <!-- Feature 1 -->
          <div class="bg-white p-8 rounded-2xl border border-gray-200 hover:border-indigo-200 hover:shadow-lg transition-all">
            <div class="w-12 h-12 bg-indigo-100 rounded-xl flex items-center justify-center mb-6">
              <svg class="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-3">Smart Task Management</h3>
            <p class="text-gray-600 leading-relaxed">
              Create, assign, and track tasks with ease. Set priorities, due dates, and custom labels to keep everything organized.
            </p>
          </div>

          <!-- Feature 2 -->
          <div class="bg-white p-8 rounded-2xl border border-gray-200 hover:border-indigo-200 hover:shadow-lg transition-all">
            <div class="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center mb-6">
              <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-3">Team Collaboration</h3>
            <p class="text-gray-600 leading-relaxed">
              Collaborate seamlessly with your team. Share projects, leave comments, and track progress in real-time.
            </p>
          </div>

          <!-- Feature 3 -->
          <div class="bg-white p-8 rounded-2xl border border-gray-200 hover:border-indigo-200 hover:shadow-lg transition-all">
            <div class="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center mb-6">
              <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-3">Advanced Analytics</h3>
            <p class="text-gray-600 leading-relaxed">
              Get insights into team productivity with detailed reports and analytics. Track performance and optimize workflows.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Testimonials -->
    <section class="py-24 bg-gray-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-20">
          <h2 class="text-4xl font-bold text-gray-900 mb-4">
            Loved by teams worldwide
          </h2>
          <p class="text-xl text-gray-600">
            See what our customers have to say about TodoShare
          </p>
        </div>

        <div class="grid md:grid-cols-3 gap-8">
          <!-- Testimonial 1 -->
          <div class="bg-white p-8 rounded-2xl border border-gray-200">
            <div class="flex items-center mb-4">
              <div class="flex text-yellow-400">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                </svg>
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                </svg>
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                </svg>
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                </svg>
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                </svg>
              </div>
            </div>
            <p class="text-gray-600 mb-6 leading-relaxed">
              "TodoShare has completely transformed how our team works. The collaboration features are outstanding and the interface is so intuitive."
            </p>
            <div class="flex items-center">
              <div class="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center text-white font-semibold mr-3">
                S
              </div>
              <div>
                <p class="font-semibold text-gray-900">Sarah Chen</p>
                <p class="text-sm text-gray-500">Product Manager, Stripe</p>
              </div>
            </div>
          </div>

          <!-- Testimonial 2 -->
          <div class="bg-white p-8 rounded-2xl border border-gray-200">
            <div class="flex items-center mb-4">
              <div class="flex text-yellow-400">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                </svg>
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                </svg>
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                </svg>
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                </svg>
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                </svg>
              </div>
            </div>
            <p class="text-gray-600 mb-6 leading-relaxed">
              "We've tried many project management tools, but TodoShare is the first one that our entire team actually loves using every day."
            </p>
            <div class="flex items-center">
              <div class="w-10 h-10 bg-green-500 rounded-full flex items-center justify-center text-white font-semibold mr-3">
                M
              </div>
              <div>
                <p class="font-semibold text-gray-900">Michael Rodriguez</p>
                <p class="text-sm text-gray-500">Engineering Lead, Shopify</p>
              </div>
            </div>
          </div>

          <!-- Testimonial 3 -->
          <div class="bg-white p-8 rounded-2xl border border-gray-200">
            <div class="flex items-center mb-4">
              <div class="flex text-yellow-400">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                </svg>
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                </svg>
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                </svg>
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                </svg>
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                </svg>
              </div>
            </div>
            <p class="text-gray-600 mb-6 leading-relaxed">
              "The analytics and reporting features give us incredible insights into our team's productivity. Game-changer for our agency."
            </p>
            <div class="flex items-center">
              <div class="w-10 h-10 bg-purple-500 rounded-full flex items-center justify-center text-white font-semibold mr-3">
                J
              </div>
              <div>
                <p class="font-semibold text-gray-900">Jessica Park</p>
                <p class="text-sm text-gray-500">Creative Director, Netflix</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="py-24 bg-indigo-600">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 class="text-4xl font-bold text-white mb-6">
          Ready to supercharge your team's productivity?
        </h2>
        <p class="text-xl text-indigo-100 mb-10 max-w-3xl mx-auto">
          Join thousands of teams who are already using TodoShare to organize their work and achieve their goals faster.
        </p>
        <div class="flex flex-col sm:flex-row justify-center gap-4 mb-8">
          <router-link 
            to="/register" 
            class="bg-white hover:bg-gray-50 text-indigo-600 px-8 py-4 rounded-xl text-lg font-semibold transition-colors"
          >
            Start your free trial
          </router-link>
          <button class="border-2 border-white text-white hover:bg-white hover:text-indigo-600 px-8 py-4 rounded-xl text-lg font-semibold transition-colors">
            Schedule a demo
          </button>
        </div>
        <p class="text-indigo-200 text-sm">
          ✓ 14-day free trial • ✓ No credit card required • ✓ Cancel anytime
        </p>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-gray-900 text-white py-16">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid lg:grid-cols-4 gap-8 mb-12">
          <!-- Logo and Description -->
          <div class="lg:col-span-2">
            <div class="flex items-center mb-6">
              <div class="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center mr-3">
                <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              <span class="text-xl font-bold">TodoShare</span>
            </div>
            <p class="text-gray-400 mb-8 max-w-md leading-relaxed">
              The productivity platform that helps teams stay organized, 
              collaborate effectively, and deliver exceptional results.
            </p>
            <div class="flex space-x-4">
              <a href="#" class="text-gray-400 hover:text-white transition-colors">
                <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.415 3.949 4.89-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.6 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.962-.695 1.797-1.562 2.457-2.549z"/>
                </svg>
              </a>
              <a href="#" class="text-gray-400 hover:text-white transition-colors">
                <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M22.46 6c-.77.35-1.6.58-2.46.69.88-.53 1.56-1.37 1.88-2.38-.83.5-1.75.85-2.72 1.05C18.37 4.5 17.26 4 16 4c-2.35 0-4.27 1.92-4.27 4.29 0 .34.04.67.11.98C8.28 9.09 5.11 7.38 3 4.79c-.37.63-.58 1.37-.58 2.15 0 1.49.75 2.81 1.91 3.56-.71 0-1.37-.2-1.95-.5v.03c0 2.08 1.48 3.82 3.44 4.21a4.22 4.22 0 0 1-1.93.07 4.28 4.28 0 0 0 4 2.98 8.521 8.521 0 0 1-5.33 1.84c-.34 0-.68-.02-1.02-.06C3.44 20.29 5.7 21 8.12 21 16 21 20.33 14.46 20.33 8.79c0-.19 0-.37-.01-.56.84-.6 1.56-1.36 2.14-2.23z"/>
                </svg>
              </a>
              <a href="#" class="text-gray-400 hover:text-white transition-colors">
                <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                </svg>
              </a>
            </div>
          </div>

          <!-- Product Links -->
          <div>
            <h3 class="text-lg font-semibold mb-6">Product</h3>
            <ul class="space-y-4 text-gray-400">
              <li><a href="#features" class="hover:text-white transition-colors">Features</a></li>
              <li><a href="#" class="hover:text-white transition-colors">Pricing</a></li>
              <li><a href="#" class="hover:text-white transition-colors">API</a></li>
              <li><a href="#" class="hover:text-white transition-colors">Integrations</a></li>
            </ul>
          </div>

          <!-- Company Links -->
          <div>
            <h3 class="text-lg font-semibold mb-6">Company</h3>
            <ul class="space-y-4 text-gray-400">
              <li><a href="#" class="hover:text-white transition-colors">About</a></li>
              <li><a href="#" class="hover:text-white transition-colors">Blog</a></li>
              <li><a href="#" class="hover:text-white transition-colors">Careers</a></li>
              <li><a href="#" class="hover:text-white transition-colors">Contact</a></li>
            </ul>
          </div>
        </div>

        <div class="border-t border-gray-800 pt-8">
          <div class="flex flex-col md:flex-row justify-between items-center">
            <p class="text-gray-400 text-sm mb-4 md:mb-0">
              © 2025 TodoShare. All rights reserved.
            </p>
            <div class="flex space-x-6 text-gray-400 text-sm">
              <a href="#" class="hover:text-white transition-colors">Privacy Policy</a>
              <a href="#" class="hover:text-white transition-colors">Terms of Service</a>
              <a href="#" class="hover:text-white transition-colors">Cookie Policy</a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">

const scrollToFeatures = () => {
  document.getElementById('features')?.scrollIntoView({ behavior: 'smooth' })
}

</script>