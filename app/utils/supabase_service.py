import os

from supabase_py import Client, create_client


class SupabaseService:
    def __init__(self, url: str, key: str):
        self.supabase: Client = create_client(url, key)

    def fetch_study(self, study_id):
        study = (
            self.supabase.table("study")
            .select("*")
            .eq("id", study_id)
            .single()
            .execute()
        )
        print(study["data"])
        return study["data"]
