<template>
  <span 
    class="category-badge" 
    :class="{ clickable: onClick }"
    :style="{ backgroundColor: category.color, borderColor: category.color }"
    @click="handleClick"
    :title="category.description || category.name"
  >
    {{ category.name }}
    <button 
      v-if="removable" 
      @click.stop="$emit('remove', category.id)"
      class="remove-btn"
      :title="`Remove ${category.name}`"
    >
      ×
    </button>
  </span>
</template>

<script setup lang="ts">
import type { Category } from '@/types/category'

interface Props {
  category: Category
  removable?: boolean
  onClick?: () => void
}

interface Emits {
  (e: 'remove', categoryId: string): void
  (e: 'click', category: Category): void
}

const props = withDefaults(defineProps<Props>(), {
  removable: false
})

const emit = defineEmits<Emits>()

const handleClick = () => {
  if (props.onClick) {
    props.onClick()
  }
  emit('click', props.category)
}
</script>

<style scoped>
.category-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
  color: white;
  border: 1px solid;
  white-space: nowrap;
  transition: all 0.2s ease;
  user-select: none;
}

.category-badge.clickable {
  cursor: pointer;
}

.category-badge.clickable:hover {
  opacity: 0.8;
  transform: translateY(-1px);
}

.remove-btn {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  padding: 0;
  width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  font-size: 12px;
  font-weight: bold;
  transition: all 0.2s ease;
  margin-left: 0.125rem;
}

.remove-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}
</style>