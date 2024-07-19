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
                 placeholder="迷人日期"
                 @click="showDatePicker"
                 class="date-field">
        <template #append>
          <van-icon name="calendar"
                    size="20"
                    color="#4caf50" />
        </template>
      </van-field>
      <van-button type="primary"
                  block
                  @click="addTodo"
                  class="add-button">添加事项</van-button>
    </van-cell-group>
    <div class="todo-list">
      <van-list>
        <van-cell v-for="todo in sortedTodos"
                  :key="todo.id"
                  :title="todo.title"
                  :label="`详细描述: ${todo.description}`"
                  is-link>
          <template #right-icon>
            <div class="actions">
              <van-button :type="todo.completed ? 'warning' : 'success'"
                          size="small"
                          icon="check"
                          @click="toggleCompletion(todo)"
                          round
                          class="action-button completion-button"
                          :class="{'completed': todo.completed}">
                <template #icon>
                  <i class="fas"
                     :class="todo.completed ? 'fa-check-square' : 'fa-square'"></i>
                </template>
              </van-button>
              <van-button type="danger"
                          size="small"
                          icon="delete"
                          @click="deleteTodo(todo.id)"
                          round
                          class="action-button delete-button"></van-button>
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
      },
    };
  },
  created () {
    this.fetchTodos();
  },
  computed: {
    sortedTodos () {
      return this.todos.slice().sort((a, b) => a.completed - b.completed || new Date(b.due_date) - new Date(a.due_date));
    }
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
      if (!this.newTodo.title || !this.newTodo.description || !this.newTodo.due_date) {
        alert('所有字段必须填写！');
        return;
      }
      axios.post('http://localhost:5001/api/todos', this.newTodo).then(response => {
        this.todos.unshift(response.data);
        this.sortTodos(); // 排序新添加的待办事项
        this.newTodo = { title: '', description: '', due_date: '', completed: false };
        alert('待办事项添加成功！');
      }).catch(error => {
        console.error('添加待办事项时出错:', error);
        alert('添加待办事项失败。');
      });
    },
    sortTodos () {
      this.todos.sort((a, b) => a.completed - b.completed || new Date(b.due_date) - new Date(a.due_date));
    },
    toggleCompletion (todo) {
      axios.put(`http://localhost:5001/api/todos/${todo.id}`, {
        ...todo,
        completed: !todo.completed
      }).then(() => {
        todo.completed = !todo.completed;
        this.sortTodos(); // 更新完成状态后重新排序
      }).catch(error => {
        console.error('更新待办事项时出错:', error);
      });
    },
    deleteTodo (id) {
      axios.delete(`http://localhost:5001/api/todos/${id}`).then(() => {
        this.todos = this.todos.filter(t => t.id !== id);
      }).catch(error => {
        console.error('删除待办事项时出错:', error);
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
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

/* 全局字体和背景 */
.container {
  font-family: 'Arial', sans-serif;
  background-color: #eef2f3;
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
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.add-button {
  margin-top: 15px;
  background-color: #4caf50;
  color: #fff;
  border: none;
  border-radius: 25px;
  padding: 15px 30px;
  font-size: 16px;
  font-weight: bold;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s ease;
}

.add-button:hover {
  background-color: #45a049;
}

/* 待办事项列表样式 */
.todo-list {
  margin-top: 20px;
  max-height: 400px;
  overflow-y: auto;
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.action-button {
  margin: 0;
  padding: 10px;
  border-radius: 15px;
  transition: background-color 0.3s ease, transform 0.3s ease;
}

.completion-button {
  background-color: #4caf50;
  color: #fff;
  font-size: 14px;
  padding: 8px 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.completion-button.completed {
  background-color: #ff9800;
}

.completion-button:hover {
  transform: scale(1.05);
}

.delete-button {
  background-color: #f44336;
  color: #fff;
  font-size: 14px;
  padding: 8px 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.delete-button:hover {
  background-color: #d32f2f;
  transform: scale(1.05);
}

.van-button span {
  margin-left: 5px;
}

/* 响应式设计 */
@media (max-width: 600px) {
  .h1-todo {
    font-size: 18px;
  }

  .van-field {
    font-size: 14px;
  }

  .add-button {
    font-size: 14px;
  }

  .todo-list {
    font-size: 14px;
  }
}

.fa-square,
.fa-check-square {
  font-size: 18px;
  color: #fff;
}
</style>

<!-- 别忘了在页面中引入 Font Awesome 库，例如通过 CDN -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
