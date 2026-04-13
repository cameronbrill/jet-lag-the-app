-- Modify "shortlinks" table
ALTER TABLE "shortlinks" ADD CONSTRAINT "shortlinks_created_by_email_fkey" FOREIGN KEY ("created_by_email") REFERENCES "users" ("email") ON UPDATE NO ACTION ON DELETE CASCADE;
