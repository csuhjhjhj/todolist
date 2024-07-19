<template>
  <div class="container">
    <h1 class="h1-todo">Todo List</h1>
    <van-cell-group>
      <van-field v-model="newTodo.title"
                 placeholder="标题"
                 clearable />
      <van-field v-model="newTodo.description"
                 placeholder="详细描述"
                 clearable />
      <van-field v-model="newTodo.due_date"
                 type="date"
                 placeholder="选择日期" />
      <van-button type="primary"
                  block
                  @click="addTodo">添加事项</van-button>
    </van-cell-group>
    <div class="todo-list">
      <van-list>
        <van-cell v-for="todo in todos"
                  :key="todo.id"
                  :title="todo.title"
                  :label="`详细描述: ${todo.description}`"
                  is-link>
          <template #right-icon>
            <div class="actions">
              <van-button type="info"
                          size="small"
                          icon="cross"
                          @click="toggleCompletion(todo)"
                          round>{{ todo.completed ? '未完成' : '完成' }}</van-button>
              <van-button type="danger"
                          size="small"
                          icon="delete"
                          @click="deleteTodo(todo.id)"
                          round>删除</van-button>
            </div>
          </template>
        </van-cell>
      </van-list>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data () {
    return {
      todos: [],
      newTodo: {
        title: '',
        description: '',
        due_date: '',
        completed: false
      }
    };
  },
  created () {
    this.fetchTodos();
  },
  methods: {
    formatDate (value) {
      return new Date(value).toLocaleDateString();
    },
    fetchTodos () {
      axios.get('http://localhost:5001/api/todos').then(response => {
        this.todos = response.data;
        this.sortTodos(); // 排序函数调用
      }).catch(error => {
        console.error('Error fetching todos:', error);
      });
    },
    addTodo () {
      console.log("Adding a new todo item");
      if (!this.newTodo.title || !this.newTodo.description || !this.newTodo.due_date) {
        alert('All fields must be filled!');
        return;
      }
      axios.post('http://localhost:5001/api/todos', this.newTodo).then(response => {
        this.todos.push(response.data);
        this.newTodo = { title: '', description: '', due_date: '', completed: false };
        alert('Todo added successfully!');
      }).catch(error => {
        console.error('Error adding todo:', error);
        alert('Failed to add todo.');
      });
    },
    sortTodos () {
      // 按完成状态排序，未完成的在前，完成的在后
      this.todos.sort((a, b) => a.completed - b.completed);
    },
    toggleCompletion (todo) {
      const updatedTodos = this.todos.map(t =>
        t.id === todo.id ? { ...t, completed: !t.completed } : t
      );

      axios.put(`http://localhost:5001/api/todos/${todo.id}`, {
        ...todo,
        completed: !todo.completed
      })
        .then(() => {
          this.todos = updatedTodos;  // 直接替换整个数组
          this.sortTodos();
        })
        .catch(error => {
          console.error("Error updating todo:", error);
        });
    },
    deleteTodo (id) {
      axios.delete(`http://localhost:5001/api/todos/${id}`).then(() => {
        this.todos = this.todos.filter(t => t.id !== id);
      }).catch(error => {
        console.error('Error deleting todo:', error);
      });
    }
  }
}
</script>

<style scoped>
/* 居中并美化标题 */
.h1-todo {
  text-align: center;
  font-size: 28px;
  color: #333;
  margin-top: 20px;
  margin-bottom: 20px;
  font-weight: bold;
  letter-spacing: 1px;
}

/* 全局字体和背景 */
.container {
  font-family: 'Arial', sans-serif;
  background-color: #f5f5f5;
  color: #333;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  max-width: 800px;
  margin: 0 auto;
}

/* 输入部分样式 */
.van-field {
  margin-bottom: 15px;
}

.van-button {
  margin-top: 15px;
}

/* 待办事项列表样式 */
.todo-list {
  margin-top: 20px;
  max-height: 400px;
  overflow-y: auto;
}

.actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.actions .van-button {
  margin: 0;
  padding: 0;
}

.van-button span {
  margin-left: 5px;
}

/* 响应式设计 */
@media (max-width: 600px) {
  .title {
    font-size: 18px;
  }

  .description,
  .date {
    font-size: 14px;
  }
}
</style>
