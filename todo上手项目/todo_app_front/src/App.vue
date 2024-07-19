<template>

  <head>
    <link rel="stylesheet"
          href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
  </head>
  <div class="layui-container">
    <!-- <h1 class="layui-header">Vue and Layui Integration</h1> -->
    <todo-list></todo-list>
  </div>
</template>

<script>
import TodoList from './components/TodoList.vue';

export default {
  name: 'App',
  components: {
    TodoList
  }
}
</script>

<style>
.layui-container {
  margin-top: 20px;
}
</style>
