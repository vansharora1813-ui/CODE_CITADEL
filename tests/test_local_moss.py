from benchmark.stores.local_moss import LocalMossClient


def test_local_moss_reset_upsert_search_contract():
    client = LocalMossClient()
    client.reset_collection("test", vector_size=3)
    client.upsert(
        "test",
        [
            {"id": "a", "vector": [1.0, 0.0, 0.0], "metadata": {"label": "x"}},
            {"id": "b", "vector": [0.0, 1.0, 0.0], "metadata": {"label": "y"}},
        ],
    )

    results = client.search("test", [0.9, 0.1, 0.0], top_k=1)

    assert results[0]["id"] == "a"
    assert results[0]["metadata"] == {"label": "x"}

