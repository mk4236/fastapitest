<script>
    import { push } from "svelte-spa-router";
    import fastapi from "../lib/api";
    import Error from "../components/Error.svelte";

    let error = { detail: [] };
    let title = "";
    let content = "";

    function post_question(event) {
        event.preventDefault();
        let url = "/api/question/";
        let params = {
            title: title,
            content: content,
        };
        fastapi(
            "post",
            url,
            params,
            (json) => {
                push("/");
            },
            (json_error) => {
                error = json_error;
            }
        );
    }
</script>

<div class="container">
    <h5 class="my-3 border-bottom pb-2">질문 등록</h5>
    <Error {error} />
    <form method="post" class="my-3">
        <div class="mb-3">
            <label for="title">제목</label>
            <input type="text" class="form-control" bind:value={title} />
        </div>
        <div class="mb-3">
            <label for="content">내용</label>
            <textarea class="form-control" rows="10" bind:value={content} />
        </div>
        <button class="btn btn-primary" on:click={post_question}>
            저장하기
        </button>
    </form>
</div>
