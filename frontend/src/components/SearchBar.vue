<template>
  <div class="search-bar">
    <div class="search-input-container">
      <div class="search-icon">🔍</div>
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search todos..."
        class="search-input"
        @input="handleSearch"
        @keyup.enter="handleEnterSearch"
        @focus="isfocused = true"
        @blur="handleBlur"
      />
      <button
        v-if="searchQuery"
        @click="clearSearch"
        class="clear-button"
        title="Clear search"
      >
        ×
      </button>
    </div>
    
    <!-- Search suggestions/history (optional) -->
    <div 
      v-if="showSuggestions && searchHistory.length > 0"
      class="search-suggestions"
    >
      <div class="suggestions-header">Recent searches</div>
      <div
        v-for="(historyItem, index) in searchHistory.slice(0, 5)"
        :key="index"
        @click="selectSuggestion(historyItem)"
        class="suggestion-item"
      >
        <span class="history-icon">🕐</span>
        <span>{{ historyItem }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { debounce } from '@/utils/debounce'

interface Emits {
  (e: 'search', query: string): void
  (e: 'clear'): void
}

const emit = defineEmits<Emits>()

const searchQuery = ref('')
const isSearching = ref(false)
const isfocused = ref(false)
const searchHistory = ref<string[]>([])

const showSuggestions = computed(() => 
  isSearching.value && searchQuery.value.length === 0 && searchHistory.value.length > 0
)

// Debounced search function
const debouncedSearch = debounce((query: string) => {
  emit('search', query)
  isSearching.value = false
}, 300)

const handleSearch = () => {
  isSearching.value = true
  debouncedSearch(searchQuery.value.trim())
}

const handleEnterSearch = () => {
  const query = searchQuery.value.trim()
  if (query) {
    addToHistory(query)
    emit('search', query)
  }
  isSearching.value = false
}

const clearSearch = () => {
  searchQuery.value = ''
  emit('clear')
  emit('search', '')
}

const handleBlur = () => {
  // Delay hiding suggestions to allow clicking on them
  setTimeout(() => {
    isSearching.value = false
  }, 200)
}

const selectSuggestion = (suggestion: string) => {
  searchQuery.value = suggestion
  emit('search', suggestion)
  isSearching.value = false
}

const addToHistory = (query: string) => {
  if (query && !searchHistory.value.includes(query)) {
    searchHistory.value.unshift(query)
    if (searchHistory.value.length > 10) {
      searchHistory.value.pop()
    }
    saveSearchHistory()
  }
}

const saveSearchHistory = () => {
  try {
    localStorage.setItem('todoSearchHistory', JSON.stringify(searchHistory.value))
  } catch (error) {
    console.warn('Failed to save search history:', error)
  }
}

const loadSearchHistory = () => {
  try {
    const stored = localStorage.getItem('todoSearchHistory')
    if (stored) {
      searchHistory.value = JSON.parse(stored)
    }
  } catch (error) {
    console.warn('Failed to load search history:', error)
  }
}

// Watch for external changes to search query
watch(() => searchQuery.value, (newValue) => {
  if (newValue === '') {
    emit('clear')
  }
})

onMounted(() => {
  loadSearchHistory()
})
</script>

<style scoped>
.search-bar {
  position: relative;
  width: 100%;
  max-width: 400px;
}

.search-input-container {
  display: flex;
  align-items: center;
  background: white;
  border: 1px solid #ddd;
  border-radius: 24px;
  padding: 0.5rem 1rem;
  transition: all 0.2s ease;
}

.search-input-container:focus-within {
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

.search-icon {
  color: #6c757d;
  margin-right: 0.5rem;
  font-size: 1rem;
}

.search-input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 1rem;
  background: transparent;
}

.search-input::placeholder {
  color: #999;
}

.clear-button {
  background: none;
  border: none;
  color: #6c757d;
  cursor: pointer;
  padding: 0;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s;
  font-size: 18px;
  margin-left: 0.5rem;
}

.clear-button:hover {
  background: #f8f9fa;
  color: #495057;
}

.search-suggestions {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #ddd;
  border-top: none;
  border-radius: 0 0 8px 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  margin-top: -1px;
}

.suggestions-header {
  padding: 0.5rem 1rem;
  font-size: 0.8rem;
  font-weight: 500;
  color: #6c757d;
  border-bottom: 1px solid #f8f9fa;
  background: #f8f9fa;
}

.suggestion-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  cursor: pointer;
  transition: background 0.2s;
  border-bottom: 1px solid #f8f9fa;
}

.suggestion-item:last-child {
  border-bottom: none;
}

.suggestion-item:hover {
  background: #f8f9fa;
}

.history-icon {
  font-size: 0.9rem;
  color: #6c757d;
}

@media (max-width: 768px) {
  .search-bar {
    max-width: 100%;
  }
  
  .search-input-container {
    border-radius: 8px;
  }
}
</style>