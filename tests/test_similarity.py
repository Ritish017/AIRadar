from backend.services.originality.similarity import originality_checker, calculate_ngram_jaccard

def test_identical_text_rejected():
    source = "OpenAI released a new reasoning model today with native computer use."
    target = "OpenAI released a new reasoning model today with native computer use."
    res = originality_checker.check_similarity(source, target)
    assert res["similarity"] >= 0.90
    assert res["is_safe"] is False

def test_near_copy_rejected():
    source = "Anthropic announces Model Context Protocol 2.0 with async streaming tools and sandboxing."
    target = "Anthropic announces Model Context Protocol 2.0 with async streaming tools and sandboxing today."
    res = originality_checker.check_similarity(source, target)
    assert res["similarity"] >= 0.70
    assert res["is_safe"] is False

def test_original_synthesis_accepted():
    source = "DeepSeek-V3 open-source model outperforms 70B competitors on coding with 671B parameters and 37B activated."
    target = "Open-weights architecture is moving at breakneck speed. The latest MoE benchmarks show that sparse activation models can rival closed frontier APIs without requiring massive multi-node inference clusters."
    res = originality_checker.check_similarity(source, target)
    assert res["similarity"] < 0.60
    assert res["is_safe"] is True

def test_ngram_jaccard():
    t1 = "the quick brown fox jumps over the lazy dog"
    t2 = "the quick brown fox leaps across the sleeping dog"
    score = calculate_ngram_jaccard(t1, t2, n=3)
    assert 0.0 < score < 1.0
