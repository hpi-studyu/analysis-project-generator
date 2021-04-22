from typing import Any, Dict

from supabase_py import Client, create_client


class SupabaseService:
    def __init__(self, url: str, key: str, session: Dict[str, Any]):
        self.supabase: Client = create_client(url, key, session)

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

    def fetch_subjects_for_study(self, study_id):
        subjects = (
            self.supabase.table("study_subject")
            .select("*", "subject_progress(*)")
            .eq("studyId", study_id)
            .execute()
        )
        print(subjects["data"])
        return subjects["data"]
