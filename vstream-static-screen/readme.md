python -m venv venv
.\venv\Scripts\activate 
pip install -r requirements.txt

uvicorn app:app --reload 
    # to run the code on 8000 port(default port)


uvicorn app:app --port 8003 --reload # vstream-static-screen
    # change the port no accordingly, check .env file for the port no

=======================================================================================================================
#screen 1
INSERT INTO public.intro_screen (
  screen_id, background_image, title, description, logo, actions
)
VALUES (
  '1',
  'D:/OTT/user/media/splash_screen/splash_img.png',
  'sample title',
  'sample description',
  'D:/OTT/user/media/splash_screen/logo.gif',
  ARRAY[]::text[]
);
=======================================================================================================================
#screen 2
INSERT INTO public.intro_screen (
  screen_id, background_image, title, description, logo, actions
)
VALUES (
  '2',
  'D:/OTT/user/media/splash_screen/splash_img.png',
  'sample title',
  'sample description',
  'D:/OTT/user/media/splash_screen/logo.gif',
  ARRAY[]::text[]
);
=======================================================================================================================
#screen 3
INSERT INTO public.intro_screen (
  screen_id, background_image, title, description, logo, actions
)
VALUES (
  '3',
  'D:/OTT/user/media/splash_screen/splash_img.png',
  'sample title',
  'sample description',
  'D:/OTT/user/media/splash_screen/logo.gif',
  ARRAY[]::text[]
);
=======================================================================================================================
