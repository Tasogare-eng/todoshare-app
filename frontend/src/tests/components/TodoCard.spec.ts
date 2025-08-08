import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import TodoCard from '@/components/TodoCard.vue'
import { TodoStatus, TodoPriority } from '@/types/todo'

const mockTodo = {
  id: '1',
  user_id: 'user1',
  title: 'Test Todo',
  description: 'Test Description',
  status: TodoStatus.PENDING,
  priority: TodoPriority.MEDIUM,
  created_at: '2024-01-01T00:00:00Z',
  categories: [
    {
      id: 'cat1',
      name: 'Work',
      color: '#007bff',
      description: 'Work tasks'
    }
  ]
}

describe('TodoCard', () => {
  it('renders todo information correctly', () => {
    const wrapper = mount(TodoCard, {
      props: {
        todo: mockTodo
      }
    })

    expect(wrapper.find('.todo-title').text()).toBe('Test Todo')
    expect(wrapper.find('.todo-description').text()).toBe('Test Description')
  })

  it('shows completed state correctly', () => {
    const completedTodo = {
      ...mockTodo,
      status: TodoStatus.COMPLETED
    }

    const wrapper = mount(TodoCard, {
      props: {
        todo: completedTodo
      }
    })

    expect(wrapper.find('.todo-card').classes()).toContain('completed')
    expect((wrapper.find('input[type="checkbox"]').element as HTMLInputElement).checked).toBe(true)
  })

  it('emits toggle event when checkbox is clicked', async () => {
    const wrapper = mount(TodoCard, {
      props: {
        todo: mockTodo
      }
    })

    await wrapper.find('input[type="checkbox"]').trigger('change')
    
    expect(wrapper.emitted('toggle')).toBeTruthy()
    expect(wrapper.emitted('toggle')?.[0]).toEqual(['1'])
  })

  it('emits delete event when delete button is clicked', async () => {
    const wrapper = mount(TodoCard, {
      props: {
        todo: mockTodo
      }
    })

    // Mock window.confirm
    vi.stubGlobal('confirm', vi.fn(() => true))

    await wrapper.find('.action-btn.delete').trigger('click')
    
    expect(wrapper.emitted('delete')).toBeTruthy()
    expect(wrapper.emitted('delete')?.[0]).toEqual(['1'])
  })

  it('shows priority indicator correctly', () => {
    const highPriorityTodo = {
      ...mockTodo,
      priority: TodoPriority.HIGH
    }

    const wrapper = mount(TodoCard, {
      props: {
        todo: highPriorityTodo
      }
    })

    expect(wrapper.find('.priority-high').exists()).toBe(true)
  })

  it('displays categories correctly', () => {
    const wrapper = mount(TodoCard, {
      props: {
        todo: mockTodo
      },
      global: {
        stubs: ['CategoryBadge']
      }
    })

    expect(wrapper.find('.todo-categories').exists()).toBe(true)
  })

  it('enters edit mode when edit button is clicked', async () => {
    const wrapper = mount(TodoCard, {
      props: {
        todo: mockTodo
      }
    })

    await wrapper.find('.action-btn.edit').trigger('click')
    
    expect(wrapper.find('.todo-edit').exists()).toBe(true)
    expect(wrapper.find('.todo-display').exists()).toBe(false)
  })
})